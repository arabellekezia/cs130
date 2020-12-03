import server from "../utils/server";
import { getUserToken } from "../utils/token";

import moment from "moment";

import { millisecondTimeStampToSeconds } from "../utils/time";

const SleepService = {
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
   * an object {year, month, day}
   * @param {*} date
   */
  getDailySleepEntries: async (date) => {
    const { year, month, day } = date;
    const startOfDate = millisecondTimeStampToSeconds(
      moment([year, month, day]).startOf("date").valueOf()
    );
    const endOfDate = millisecondTimeStampToSeconds(
      moment([year, month, day]).endOf("date").valueOf()
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
};

export default SleepService;
