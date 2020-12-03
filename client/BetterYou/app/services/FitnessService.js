import server from "../utils/server";
import { getUserToken } from "../utils/token";

const FitnessService = {
  getFitnessEntries: async (dateFrom, dateTo) => {
    try {
      const res = await server.post("/getFitnessData", formdata, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        params: {
          token: await getUserToken(),
          dateFrom,
          dateTo,
        },
      });
      return res.body;
    } catch (err) {
      console.log(err);
      return null;
    }
  },
  addFitnessEntry: async (weight, duration, type) => {
    const formdata = new FormData();
    formdata.append("token", await getUserToken());
    formdata.append("weight", weight);
    formdata.append("minutes", duration);
    formdata.append("workout", type);

    try {
      await server.post("/enterWorkout", formdata, {
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
  getDailyFitnessEntries: async () => {
    const today = DateUtils.getTodayTimeRange();
    return await FitnessService.getFitnessEntries(today.dateFrom, today.dateTo);
  },
};

export default FitnessService;
