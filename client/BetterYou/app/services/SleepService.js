import server from "../utils/server";
import { getUserToken } from "../utils/token";

import moment from "moment";

import { millisecondTimeStampToSeconds } from "../utils/time";
import DateUtils from "../utils/date";

/** @module SleepService */
const SleepService = {
  /**
   * POST request to add sleep entries with the parameters for the user specified with token
   * @param {Date} startDate Start date of sleep
   * @param {Date} endDate End date of sleep
   * @param {boolean} nap Whether it is a nap or not
   * @return {boolean} true - success, false - fail
   */ 
  addSleepEntry: async (startDate, endDate, nap) => {
    const formdata = new FormData();
    formdata.append("token", await getUserToken());
    formdata.append("dateFrom", startDate);
    formdata.append("dateTo", endDate);
    formdata.append("nap", nap);

    try {
      await server.post("/insertSleepEntry", formdata, {
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
   * GET request to get sleep entries of the certain day
   * @param {Number} date: the number of milliseconds since the Unix Epoch (Jan 1 1970 12AM UTC).
   * @return {Array} Array of sleep entries
   */ 
  getDailySleepEntries: async (date) => {
    const startOfDate = millisecondTimeStampToSeconds(
      moment(date).startOf("date").valueOf()
    );
    const endOfDate = millisecondTimeStampToSeconds(
      moment(date).endOf("date").valueOf()
    );

    try {
      const params = {
        token: await getUserToken(),
        dateFrom: startOfDate,
        dateTo: endOfDate,
      };

      const res = await server.get("/getSleepData", { params: params });
      return res.data;
    } catch (err) {
      throw new Error(err);
    }
  },
  /**
   * uses getDailySleepEntries() to get all sleep entries for a given week
   * @return {Array} Array of sleep entries for the week, each index for one day
   */ 
  getWeeklySleepEntries: async () => {
    const days = DateUtils.getDaysInWeek();
    const res = [];
    for (let i = 0; i < days.length; i++) {
      try {
        res[i] = await SleepService.getDailySleepEntries(days[i].valueOf());
      } catch (err) {
        throw new Error(err);
      }
    }
    return res;
  },
};

export default SleepService;
