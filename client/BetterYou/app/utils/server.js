import Constants from "expo-constants";
import axios from "axios";
const { manifest } = Constants;

// Must specify the actual IP address the server runs on
// localhost does not suffice for Android emulated devices
let server = axios.create({
  baseURL: `http://${manifest.debuggerHost.split(":").shift()}:5000`,
  timeout: 10000,
});

export default server;
