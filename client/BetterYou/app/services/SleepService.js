import server from "../utils/server";
import { getUserToken } from "../utils/token";

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
};

export default SleepService;
