import AsyncStorage from "@react-native-async-storage/async-storage";

const TOKEN_KEY = "user_token_key";

async function storeUserToken(token) {
  try {
    await AsyncStorage.setItem(TOKEN_KEY, token);
  } catch (err) {
    console.log(err);
  }
}

async function getUserToken() {
  try {
    const userToken = await AsyncStorage.getItem(TOKEN_KEY);
    if (!userToken) {
      console.log(
        "There is no JWT user token stored locally yet, login to obtain!"
      );
    }
    return userToken;
  } catch (err) {
    console.log(err);
  }
}

export { storeUserToken, getUserToken };
