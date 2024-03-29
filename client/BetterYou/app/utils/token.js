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

async function clearUserToken() {
  try {
    await AsyncStorage.removeItem(TOKEN_KEY);
  } catch (err) {
    throw new Error(err);
  }
}

export { storeUserToken, getUserToken, clearUserToken };
