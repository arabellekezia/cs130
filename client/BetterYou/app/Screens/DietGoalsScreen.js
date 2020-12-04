import React from "react";
import { SafeAreaView, StyleSheet, View, Text, Linking } from "react-native";
import { ScrollView } from "react-native-gesture-handler";
import AppText from "../components/AppText";
import AppTextInput from "../components/AppTextInput";
import TextButton from "../components/TextButton";
import TitleText from "../components/TitleText";
import GoalsService from "../services/GoalsService";


const MIN_CALORIES = 1000;

function DietGoalsScreen({ navigation }) {
  const [calorieGoal, setCalorieGoal] = React.useState(0);
  const [err, setError] = React.useState({ calorieBudget: false });

  async function save() {
    const validCalorieGoal =
      calorieGoal > MIN_CALORIES && Boolean(Number(calorieGoal));
    if (!validCalorieGoal) {
      setError({ calorieBudget: true });
      return;
    }
    await GoalsService.setCalorieGoal(calorieGoal);
    navigation.popToTop();
  }

  function resetErrors() {
    setError({ calorieBudget: false });
  }

  function displayErrorMessage(err) {
    if (err.calorieBudget) {
      if (calorieGoal <= MIN_CALORIES) {
        return (
          <ErrorMessage message="Your daily calorie budget must be greater than 1000 calories." />
        );
      }
      if (!Boolean(Number(calorieGoal))) {
        return (
          <ErrorMessage message="Your daily calorie budget must be a number." />
        );
      }
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
        <TitleText style={styles.pageTitle} children="Diet Goals" />
        <View style={styles.form}>
          <AppText
            style={styles.question}
            children="What is your daily calorie budget?"
          />
          <AppTextInput
            style={styles.textInput}
            placeholder="2000 cal"
            isError={err.calorieBudget}
            keyboardType="numeric"
            onChangeText={(calories) => {
              setCalorieGoal(calories);
              resetErrors();
            }}
          />
          {displayErrorMessage(err)}
          <HealthInfo style={styles.healthInfoContainer} />
        </View>
        <TextButton
          style={styles.saveButton}
          name="Save"
          onPress={async () => {
            await save();
          }}
        />
      </SafeAreaView>
    </ScrollView>
  );
}

function ErrorMessage({ message }) {
  return (
    <AppText
      style={{
        alignSelf: "flex-start",
        marginLeft: "2.5%",
        color: "red",
      }}
      testID="error-message"
      children={message}
    />
  );
}

function HealthInfo({ style }) {
  const calorieCalculatorLink =
    "https://www.calculator.net/calorie-calculator.html";
  return (
    <View style={style}>
      <Text style={styles.informationalTextHeader}>
        New to calorie counting?
      </Text>
      <Text style={styles.informationalText}>
        <Text style={styles.informationalText}>{"Use the following "}</Text>
        <Text
          style={styles.learnMoreText}
          onPress={() => {
            Linking.openURL(calorieCalculatorLink);
          }}
        >
          {"calorie calculator"}
        </Text>
        <Text>
          {
            " as a guideline to determine your daily calorie intake based on your weight loss goals!"
          }
        </Text>
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "white",
    alignItems: "center",
    justifyContent: "center",
  },
  pageTitle: {
    alignSelf: "flex-start",
    marginTop: "5%",
    marginLeft: "5%",
  },
  form: {
    flex: 1,
    width: "90%",
    alignItems: "center",
    flexDirection: "column",
  },
  question: {
    alignSelf: "flex-start",
    marginTop: "10%",
    marginBottom: "2%",
    color: "#474747",
    fontSize: 18,
    fontWeight: "bold",
  },
  healthInfoContainer: {
    marginTop: "10%",
    padding: "5%",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#eafbff",
    borderRadius: 24,
  },
  informationalTextHeader: {
    fontSize: 18,
    color: "#474747",
    textAlign: "center",
    fontWeight: "bold",
  },
  informationalText: {
    fontSize: 16,
    color: "#474747",
    textAlign: "left",
    marginTop: "5%",
    lineHeight: 26,
  },
  learnMoreText: {
    fontSize: 16,
    color: "#0079d3",
    textDecorationLine: "underline",
  },
  saveButton: {
    alignSelf: "flex-end",
    marginBottom: "10%",
    minWidth: "90%",
  },
});

export default DietGoalsScreen;
