import Constants from "expo-constants";
import axios from "axios";
const { manifest } = Constants;

// Must specify the actual IP address the server runs on
// localhost does not suffice for Android emulated devices
let server = axios.create({
  baseURL: `http://${manifest.debuggerHost.split(":").shift()}:5000`,
  timeout: 10000,
});

server.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response.status == 401) {
      console.log("Expired JWT token!");
      // i want to redirect user to the login screen if their token is expired, but i don't think this is possible
      // even if i use a top level navigator
    }
    throw err;
  }
);

export default server;
