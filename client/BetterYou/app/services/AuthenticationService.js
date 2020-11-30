import server from "../utils/server";
import { storeUserToken } from "../utils/token";

const AuthenticationService = {
  login: async (email, password) => {
    let loginData = new FormData();
    loginData.append("email", email);
    loginData.append("password", password);

    try {
      const loginResponse = await server.post("/auth/login", loginData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      await storeUserToken(loginResponse.data);
      console.log("Successfully logged in!");
      return true;
    } catch (err) {
      if (err.response.status === 400) {
        console.log("Incorrect credentials!");
      }
      return false;
    }
  },
  signup: async (fullName, email, password) => {
    let registerData = new FormData();
    registerData.append("fullname", fullName);
    registerData.append("email", email);
    registerData.append("password", password);

    try {
      await server.post("/register", registerData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      console.log("Successfully signed up!");
    } catch (err) {
      console.log(err);
      return false;
    }

    let loginData = new FormData();
    loginData.append("email", email);
    loginData.append("password", password);

    await AuthenticationService.login(email, password);
    return true;
  },
};

export default AuthenticationService;
