import server from "../utils/server";
import { getUserToken } from "../utils/token";
import DateUtils from "../utils/date";
import moment from "moment";

let myMap = new Map([
  [1, "one"],
  [2, "two"],
  [3, "three"],
]);

// return
// { label: "Cycling", value: "Bicycling: 12-13.9 mph" },
// { label: "Hiking", value: "Hiking: cross country" },
// { label: "Jogging", value: "Running: 6 min/mile" },
// { label: "Sprinting", value: "Running: 10 min/mile" },
// { label: "Swimming", value: "Swimming: laps, vigorous" },
// { label: "Walking", value: "Walk: 15 min/mile" },
// { label: "Weightlifting", value: "Weightlifting: general" },
// ];
const activityNameToAPIActivity = new Map([
  ["Cycling", "Bicycling: 12-13.9 mph"],
  ["Hiking", "Hiking: cross country"],
  ["Jogging", "Running: 6 min/mile"],
  ["Sprinting", "Running: 10 min/mile"],
  ["Swimming", "Swimming: laps, vigorous"],
  ["Walking", "Walk: 15 min/mile"],
  ["Weightlifting", "Weightlifting: general"],
]);

const APIActivityToActivityName = new Map([
  ["Bicycling: 12-13.9 mph", "Cycling"],
  ["Hiking: cross country", "Hiking"],
  ["Running: 6 min/mile", "Jogging"],
  ["Running: 10 min/mile", "Sprinting"],
  ["Swimming: laps, vigorous", "Swimming"],
  ["Walk: 15 min/mile", "Walking"],
  ["Weightlifting: general", "Weightlifting"],
]);

const FitnessService = {
  getFitnessEntries: async (dateFrom, dateTo) => {
    try {
      const res = await server.get("/getFitnessData", {
        params: {
          token: await getUserToken(),
          dateFrom,
          dateTo,
        },
      });
      const entries = res.data.map((entry) => {
        entry.WorkoutType = APIActivityToActivityName.get(entry.WorkoutType);
        return entry;
      });
      return entries;
    } catch (err) {
      console.log(err);
      return null;
    }
  },
  addFitnessEntry: async (weight, activeTime, category) => {
    const formdata = new FormData();
    formdata.append("token", await getUserToken());
    formdata.append("weight", weight);
    formdata.append("minutes", activeTime);
    formdata.append("workout", category);

    try {
      await server.post("/enterWorkout", formdata, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
    } catch (err) {
      console.log(err);
    }
  },
  getDailyFitnessEntries: async (day = moment()) => {
    const today = DateUtils.getDayTimeRange(day);
    return await FitnessService.getFitnessEntries(today.dateFrom, today.dateTo);
  },
  getWeeklyFitnessEntries: async () => {
    const week = DateUtils.getDaysInWeek();
    let results = [];
    week.forEach((day) => {
      const date = DateUtils.getDayTimeRange(day);
      results.push(
        FitnessService.getFitnessEntries(date.dateFrom, date.dateTo)
      );
    });
    const weeklyEntries = await Promise.all(results);
    console.log(weeklyEntries);
    return weeklyEntries.map((dayEntries) => {
      let caloriesBurned = 0;
      let activeTime = 0;
      dayEntries.forEach((entry) => {
        caloriesBurned += entry.CaloriesBurned;
        activeTime += entry.Minutes;
      });
      return { caloriesBurned, activeTime };
    });
  },
};

export default FitnessService;
