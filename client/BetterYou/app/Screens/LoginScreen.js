import React, { useContext } from "react";
import { SafeAreaView, StyleSheet, Text } from "react-native";
import { ScrollView } from "react-native-gesture-handler";
import AppText from "../components/AppText";
import AppTextInput from "../components/AppTextInput";
import TextButton from "../components/TextButton";
import AuthContext from "../context/AuthContext";
import AuthenticationService from "../services/AuthenticationService";

function LoginScreen({ navigation }) {
  const authContext = useContext(AuthContext);

  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [err, setError] = React.useState({ email: false, password: false });

  async function login() {
    if (!validate(email, password, setError)) {
      console.log(err);
      return;
    }

    const isSuccess = await AuthenticationService.login(email, password);
    if (isSuccess) {
      authContext.setIsSignedIn(true);
    } else {
      setError({ email: true, password: true });
    }
  }

  function displayErrorMessage(err) {
    if (err.email || err.password) {
      return <ErrorMessage message="Incorrect email or password." />;
    }
  }

  return (
    <ScrollView
      contentContainerStyle={{
        flex: 1,
      }}
      keyboardShouldPersistTaps="handled"
    >
      <SafeAreaView style={styles.container}>
        <AppText
          style={{
            alignSelf: "flex-start",
            marginLeft: "5%",
            marginBottom: "5%",
            fontSize: 34,
          }}
          children="Welcome!"
        />
        <AppTextInput
          style={styles.textInput}
          placeholder="Email"
          autoCapitalize="none"
          keyboardType="email-address"
          icon="account"
          isError={err.email || err.password}
          autoFocus={true}
          onChangeText={(email) => {
            setEmail(email);
            setError({ email: false, password: false });
          }}
        />
        <AppTextInput
          style={styles.textInput}
          placeholder="Password"
          icon="lock"
          onChangeText={(password) => {
            setPassword(password);
            setError({ email: false, password: false });
          }}
          isError={err.email || err.password}
          secureTextEntry={true}
        />
        {displayErrorMessage(err)}
        <TextButton
          style={styles.submitButton}
          name="Login"
          onPress={async () => {
            await login();
          }}
        />
        <Text style={{ marginVertical: "5%" }}>
          Don't have an account?
          <Text
            style={{ color: "#0079d3" }}
            onPress={() => {
              console.log("Navigate to the signup screen");
              navigation.navigate("Signup");
            }}
          >
            {" Sign up!"}
          </Text>
        </Text>
      </SafeAreaView>
    </ScrollView>
  );
}

function ErrorMessage({ message }) {
  return (
    <AppText
      style={{
        alignSelf: "flex-start",
        marginLeft: "6%",
        color: "red",
      }}
      children={message}
    />
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "white",
    alignItems: "center",
    justifyContent: "center",
  },
  textInput: {
    width: "90%",
  },
  submitButton: { marginVertical: 12, minWidth: "90%" },
});

function validateEmail(email) {
  const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(String(email).toLowerCase());
}

function validate(email, password, setError) {
  const validEmail = validateEmail(email);
  const validPassword = Boolean(password);
  setError({ email: !validEmail, password: !validPassword });
  return validEmail && validPassword;
}

export default LoginScreen;
