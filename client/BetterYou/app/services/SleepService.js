import server from "../utils/server";
import { getUserToken } from "../utils/token";

import moment from "moment";

import { millisecondTimeStampToSeconds } from "../utils/time";
import DateUtils from "../utils/date";

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
   *
   * @param {Number} date: the number of milliseconds since the Unix Epoch (Jan 1 1970 12AM UTC).
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
