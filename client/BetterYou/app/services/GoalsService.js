import server from "../utils/server";
import { getUserToken } from "../utils/token";

const DIET_GOAL_TYPE = "Calories";
const FITNESS_GOAL_TYPE = "FitnessMinutes";
const SLEEP_GOAL_TYPE = "SleepHours";

const GoalsService = {
  setGoal: async (goalType, value) => {
    const formdata = new FormData();
    formdata.append("token", await getUserToken());
    formdata.append("type", goalType);
    formdata.append("value", value);

    try {
      await server.post("/changeGoal", formdata, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
    } catch (err) {
      console.log(err);
      return false;
    }
    return true;
  },
  setCalorieGoal: async (calories) => {
    const isSuccess = await GoalsService.setGoal(DIET_GOAL_TYPE, calories);
    if (isSuccess) {
      console.log(`Successfully set new diet goal of ${calories} calories.`);
    } else {
      console.log("Could not set diet goal.");
    }
  },
  setActiveTimeGoal: async (activeTime) => {
    const isSuccess = await GoalsService.setGoal(FITNESS_GOAL_TYPE, activeTime);
    if (isSuccess) {
      console.log(`Successfully set fitness goal of ${activeTime} active min.`);
    } else {
      console.log("Could not set fitness goal.");
    }
  },
  setSleepDurationGoal: async (duration) => {
    const isSuccess = await GoalsService.setGoal(SLEEP_GOAL_TYPE, duration);
    if (isSuccess) {
      console.log(
        `Successfully set sleep goal of ${duration} hours per night.`
      );
    } else {
      console.log("Could not set sleep goal.");
    }
  },
};

export default GoalsService;
