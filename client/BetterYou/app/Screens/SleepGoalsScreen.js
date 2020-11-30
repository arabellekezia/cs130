import React from "react";
import { SafeAreaView, StyleSheet, View, Text, Linking } from "react-native";
import AppText from "../components/AppText";
import AppTextInput from "../components/AppTextInput";
import TextButton from "../components/TextButton";
import TitleText from "../components/TitleText";
import GoalsService from "../services/GoalsService"; 

const MIN_SLEEP_TIME = 0;

function SleepGoalsScreen() {
  const [sleepHours, setSleepHours] = React.useState(0);
  const [err, setError] = React.useState({ sleepHours: false });

  async function save() {
    const validSleepHours =
      sleepHours > MIN_SLEEP_TIME &&
      sleepHours <= 24 &&
      Boolean(Number(sleepHours));
    if (!validSleepHours) {
      setError({ sleepHours: true });
      return;
    }
    await GoalsService.setSleepDurationGoal(sleepHours);
  }

  function resetErrors() {
    setError({ sleepHours: false });
  }

  function displayErrorMessage(err) {
    if (err.sleepHours) {
      if (sleepHours <= MIN_SLEEP_TIME) {
        return (
          <ErrorMessage message="Your goal must be greater than 0 hours per night." />
        );
      }

      if (sleepHours > 24) {
        return (
          <ErrorMessage message="Your goal must be less than 24 hours per night." />
        );
      }
      if (!Boolean(Number(sleepHours))) {
        return <ErrorMessage message="Your goal must be a number." />;
      }
    }
  }

  return (
    <SafeAreaView style={styles.container}>
      <TitleText style={styles.header} children="Sleep Goals" />
      <View style={styles.form}>
        <AppText
          style={styles.question}
          children="What is your target number of hours of sleep per night?"
        />
        <AppTextInput
          style={styles.textInput}
          placeholder="7 hours"
          isError={err.sleepHours}
          keyboardType="numeric"
          onChangeText={(sleepHours) => {
            setSleepHours(sleepHours);
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
      children={message}
    />
  );
}

function HealthInfo({ style }) {
  const sleepDurationLink =
    "https://www.cdc.gov/sleep/about_sleep/how_much_sleep.html";
  return (
    <View style={style}>
      <Text style={styles.informationalTextHeader}>
        Recommended sleep duration
      </Text>
      <Text style={styles.informationalText}>
        <Text style={styles.informationalText}>
          <Text>
            The amount of sleep needed is different for everybody. The CDC
            recommends that adults aim for
          </Text>
          <Text style={{ fontWeight: "bold" }}>{" 7 or more hours "}</Text>
          per night.
        </Text>
      </Text>
      <Text
        style={styles.learnMoreText}
        onPress={() => {
          Linking.openURL(sleepDurationLink);
        }}
      >
        {"Learn more"}
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
  header: {
    alignSelf: "flex-start",
    marginTop: "15%",
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
    textAlign: "center",
    marginTop: "5%",
    textDecorationLine: "underline",
  },
  saveButton: {
    alignSelf: "flex-end",
    marginBottom: "10%",
    minWidth: "90%",
  },
});

export default SleepGoalsScreen;
