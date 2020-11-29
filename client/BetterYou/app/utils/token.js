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
    return await AsyncStorage.getItem(TOKEN_KEY);
  } catch (err) {
    console.log(err);
  }
}

export { storeUserToken, getUserToken };
