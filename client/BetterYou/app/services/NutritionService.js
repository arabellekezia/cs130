import server from "../utils/server";
import { getUserToken } from "../utils/token";

const NutritionService = {
  // sends POST request to add the meal that is chosen by user
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
  // sends GET request to gets the meals logged within the user database that are within the dates listed
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
  /*
    sends GET request to get {nMatches} number of food items from our API that most closely matches the {item}
    the ServingSize serves as a multiplier, but it should most likely always be set to 1 as we are getting the labels
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
  /*
    sends GET request to get nutrition facts of the from our API that most closely matches the {item}
    the ServingSize serves as a multiplier
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
