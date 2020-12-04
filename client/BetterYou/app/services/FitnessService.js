import server from "../utils/server";
import { getUserToken } from "../utils/token";
import DateUtils from "../utils/date";
import moment from "moment";


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
  /**
   * GET request to get fitness entries from the specified date interval for the user specified with token
   * @param {Unix Timestamp} dateFrom The date to fetch data from
   * @param {Unix Timestamp} dateTo The date to fetch data to
   * @return {Map} The fitness entries fetched from database
   */ 
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
  /**
   * POST request to add fitness entries with the parameters for the user specified with token
   * @param {number} weight Weight of user
   * @param {number} activeTime Time active in minutes
   * @param {string} category The category of the workout
   * @return {void}
   */ 
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
  /**
   * Helper function that uses getFitnessEntries to get fitness entries for a single day
   * @param {moment object} [day = moment()] The day date to fetch data from
   * @return {Map} The fitness entries fetched from database
   */ 
  getDailyFitnessEntries: async (day = moment()) => {
    const today = DateUtils.getDayTimeRange(day);
    return await FitnessService.getFitnessEntries(today.dateFrom, today.dateTo);
  },
  /**
   * Helper function that uses getFitnessEntries to get fitness entries for a given week
   * @return {Map} The fitness entries fetched from database and processed to return a Map of {caloriesBurned, activeTime} per day in week
   */ 
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
