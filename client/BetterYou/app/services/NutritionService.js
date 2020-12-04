import server from "../utils/server";
import { getUserToken } from "../utils/token";
import DateUtils from "../utils/date";
import moment from "moment";

const NutritionService = {
  /**
   * sends POST request to add the meal that is chosen by user
   * @param {string} fooditem Name (or barcode if barcode = true) of the food item
   * @param {number} servingsize The number of serving sizes consumed
   * @param {string} barcode set to "true" if barcode is used in fooditem, anything else if not
   * @return {boolean} true - success, false - failure
   */ 
  addMeals: async (fooditem, servingsize, barcode) => {
    const formdata = new FormData();
    formdata.append("token", await getUserToken());
    formdata.append("item", fooditem);
    formdata.append("ServingSize", servingsize);
    formdata.append("barcode", barcode);  //if barcode is true then item will be replaced with the barcode

    try {
      await server.post("/addMeal", formdata, {
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
  // 
  /**
   * sends GET request to gets the meals logged within the user database that are within the dates listed
   * @param {Unix Timestamp} dateFrom The date to fetch data from
   * @param {Unix Timestamp} dateTo The date to fetch data to
   * @return {List} A list of all foods in that date interval with its name and stats compiled in an object
   */ 
  getMeals: async (dateFrom, dateTo) => {
    try {
      const res = await server.get("/getMeals", {
        params: {
          token: await getUserToken(),
          dateFrom,
          dateTo,
        },
      });
      // res.data returns the data in an [{fooditemandinfo1}, {fooditemandinfo2}, ...] that falls within the date interval
      return res.data;
    } catch (err) {
      console.log(err);
      return null;
    }
  },
  /**
   * Helper function to call getMeals specified for the single day
   * @param {moment object} [day = moment()] The day date to fetch data from
   * @return {List} The food entries fetched from database
   */ 
  getDailyMealEntries: async (day = moment()) => {
    const today = DateUtils.getDayTimeRange(day);
    return await NutritionService.getMeals(today.dateFrom, today.dateTo);
  },
  /**
   * Helper function that uses getMeals to get data needly for weekly nutrition pages
   * @return {Map} The fitness entries fetched from database and processed to return a Map of {caloriesBurned, activeTime} per day in week
   */ 
  getWeeklyNutritionEntries: async () => {
    const week = DateUtils.getDaysInWeek();
    let results = [];
    week.forEach((day) => {
      const date = DateUtils.getDayTimeRange(day);
      results.push(
        NutritionService.getMeals(date.dateFrom, date.dateTo)
      );
    });
    const weeklyEntries = await Promise.all(results);
    //console.log(weeklyEntries);
    return weeklyEntries.map((dayEntries) => {
      let dailyCals = 0;
      let dailyCarbs = 0;
      let dailyProtein = 0;
      let dailyFat = 0;
      dayEntries.forEach((entry) => {
        dailyCals += entry.Cals;
        dailyCarbs += entry.Carbs;
        dailyProtein += entry.Protein;
        dailyFat += entry.Fat;
      });
      return { dailyCals, dailyCarbs, dailyProtein, dailyFat };
    });
  },
   /**
   * sends GET request to get closest matched food items from our API that most closely matches
   * @param {string} item Item name
   * @param {number} nMatches Number of closest matches returned
   * @param {number} ServingSize How many servings; should most likely always be set to 1 as we are getting the labels
   * @return {Object} An object list of nMatches foods its name and stats compiled in an object
   */ 
  getAvailableFoods: async (item, nMatches, ServingSize) => {
    try {
      const res = await server.get("/getAvailableFoods", {
        params: {
          item,
          nMatches,
          ServingSize,
        },
      });
      /* res.data returns the data in the form of;
        { key(index from 0): {"Label": foodname, "Nutrients": {...}} , ... }
        for n number of matches from nMatches
      */
      return res.data;
    } catch (err) {
      console.log(err);
      return null;
    }
  },
  /**
  * sends GET request to get nutritional data of a food item by either barcode or name
  * @param {string} item Item name
  * @param {number} ServingSize Serving size to multiply by for nutrition facts
  * @param {string} barcode "true" or anything else (optional)
  * @return {Object} An object of the matching food its name and stats
  */ 
 getNutritionalData: async (item, ServingSize, barcode) => {
  try {
    const res = await server.get("/getNutritionalData", {
      params: {
        item,
        ServingSize,
        barcode,  // if barcode is set to "true" the item parameter should be the barcode number
      },
    });
    /* res.data returns the data in the form of;
      { "0": {"Label": foodname, "Nutrients": {"Cals": , "Protein": , "Fat": , "Carbs": , "Fiber": }}}
    */
    return res.data;
  } catch (err) {
    console.log(err);
    return null;
  }
},
};

export default NutritionService;
