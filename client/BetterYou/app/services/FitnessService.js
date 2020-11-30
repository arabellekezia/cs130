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
};

export default FitnessService;
