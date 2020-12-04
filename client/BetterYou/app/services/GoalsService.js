import server from "../utils/server";
import { getUserToken } from "../utils/token";

const DIET_GOAL_TYPE = "Calories";
const FITNESS_GOAL_TYPE = "FitnessMinutes";
const SLEEP_GOAL_TYPE = "SleepHours";

/** @module GoalsService */
const GoalsService = {
  /**
   * General function that sends a POST request to set goal with the parameters in the user's database
   * @param {string} goalType Specifies the type of goal we are setting
   * @param {number} value The goal number
   * @return {boolean} true - success, false - failure
   */ 
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
  /**
   * General function that sends a GET request to get goal with the parameters for the user specified with token
   * @param {string} type Specifies the type of goal we are getting
   * @return {number} The goal value
   */ 
  getGoal: async (type) => {
    try {
      const response = await server.get("/getTypeGoals", {
        params: {
          token: await getUserToken(),
          type,
        },
      });
      return response.data[0].Value;
    } catch (err) {
      console.log(err);
    }
  },
  /**
   * Returns the logged in user's goals as {calories, activeTime, sleepDuration}.
   * @return {Object} Goals in separate indices
   */ 
  getAllGoals: async () => {
    try {
      const response = await server.get("/getAllGoals", {
        params: {
          token: await getUserToken(),
        },
      });
      let goals = {};
      response.data.forEach((goal) => {
        switch (goal.Type) {
          case DIET_GOAL_TYPE:
            goals.calories = goal.Value;
            break;
          case FITNESS_GOAL_TYPE:
            goals.activeTime = goal.Value;
            break;
          case SLEEP_GOAL_TYPE:
            goals.sleepDuration = goal.Value;
            break;
        }
      });
      return goals;
    } catch (err) {
      console.log(err);
    }
  },
  /**
   * Helper that calls getGoal() for only Calorie goals
   * @return {number} The goal value
   */ 
  getCalorieGoal: async () => {
    return await GoalsService.getGoal(DIET_GOAL_TYPE);
  },
  /**
   * Helper that calls getGoal() for only Fitness goals
   * @return {number} The goal value
   */ 
  getActiveTimeGoal: async () => {
    return await GoalsService.getGoal(FITNESS_GOAL_TYPE);
  },
  /**
   * Helper that calls getGoal() for only Sleep goals
   * @return {number} The goal value
   */ 
  getSleepDurationGoal: async () => {
    return await GoalsService.getGoal(SLEEP_GOAL_TYPE);
  },
  /**
   * Helper that calls setGoal() for only Calorie goals
   * @param {number} calories Calories to set as goal
   * @return {void}
   */ 
  setCalorieGoal: async (calories) => {
    const isSuccess = await GoalsService.setGoal(DIET_GOAL_TYPE, calories);
    if (isSuccess) {
      console.log(`Successfully set new diet goal of ${calories} calories.`);
    } else {
      console.log("Could not set diet goal.");
    }
  },
  /**
   * Helper that calls setGoal() for only Fitness goals
   * @param {number} activeTime Minutes of Active Time to set as goal
   * @return {void}
   */ 
  setActiveTimeGoal: async (activeTime) => {
    const isSuccess = await GoalsService.setGoal(FITNESS_GOAL_TYPE, activeTime);
    if (isSuccess) {
      console.log(`Successfully set fitness goal of ${activeTime} active min.`);
    } else {
      console.log("Could not set fitness goal.");
    }
  },
  /**
   * Helper that calls setGoal() for only Sleep Duration goals
   * @param {number} duration Minutes of Sleep to set as goal
   * @return {void}
   */ 
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
