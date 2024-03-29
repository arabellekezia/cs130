import React from "react";
import { SafeAreaView, StyleSheet, View, Text, Linking } from "react-native";
import { ScrollView } from "react-native-gesture-handler";
import AppText from "../components/AppText";
import AppTextInput from "../components/AppTextInput";
import TextButton from "../components/TextButton";
import TitleText from "../components/TitleText";
import GoalsService from "../services/GoalsService";

const MIN_ACTIVE_TIME = 0;
const MAX_ACTIVE_TIME = 1440;

function FitnessGoalsScreen({ navigation }) {
  const [activeTimeGoal, setActiveTimeGoal] = React.useState(0);
  const [err, setError] = React.useState({ activeTime: false });

  async function save() {
    const validActiveTimeGoal =
      activeTimeGoal > MIN_ACTIVE_TIME &&
      activeTimeGoal < MAX_ACTIVE_TIME &&
      Boolean(Number(activeTimeGoal));

    if (!validActiveTimeGoal) {
      setError({ activeTime: true });
      return;
    }
    await GoalsService.setActiveTimeGoal(activeTimeGoal);
    navigation.popToTop();
  }

  function resetErrors() {
    setError({ activeTime: false });
  }

  function displayErrorMessage(err) {
    if (err.activeTime) {
      if (activeTimeGoal <= MIN_ACTIVE_TIME) {
        return (
          <ErrorMessage message="Your daily active time goal must be greater than 0 minutes." />
        );
      }

      if (activeTimeGoal > MAX_ACTIVE_TIME) {
        return (
          <ErrorMessage
            message={`Your daily active time goal cannot exceed ${MAX_ACTIVE_TIME} minutes.`}
          />
        );
      }

      if (!Boolean(Number(activeTimeGoal))) {
        return (
          <ErrorMessage message="Your daily active time goal must be a number." />
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
        <TitleText style={styles.pageTitle} children="Fitness Goals" />
        <View style={styles.form}>
          <AppText
            style={styles.question}
            children="What is your daily active minutes goal?"
          />
          <AppTextInput
            style={styles.textInput}
            placeholder="30 minutes"
            isError={err.activeTime}
            keyboardType="numeric"
            onChangeText={(activeTime) => {
              setActiveTimeGoal(activeTime);
              resetErrors();
            }}
          />
          {displayErrorMessage(err)}
          <HealthInfo style={styles.healthInfoContainer} />
        </View>
        <TextButton
          style={styles.saveButton}
          name="Save"
          onPress={async () => await save()}
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
  const activeTimeLink =
    "https://www.heart.org/en/healthy-living/fitness/fitness-basics/aha-recs-for-physical-activity-in-adults";
  return (
    <View style={style}>
      <Text style={styles.informationalTextHeader}>
        Recommended active minutes
      </Text>
      <Text style={styles.informationalText}>
        <Text style={styles.informationalText}>
          <Text>The American Heart Association recommends at least </Text>
          <Text style={{ fontWeight: "bold" }}>{"150 minutes per week "}</Text>
          of moderate-intensity aerobic activity or
          <Text style={{ fontWeight: "bold" }}>{" 75 minutes per week "}</Text>
          {"of vigorous aerobic activity. "}
        </Text>
      </Text>
      <Text
        style={styles.learnMoreText}
        onPress={() => {
          Linking.openURL(activeTimeLink);
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

export default FitnessGoalsScreen;
