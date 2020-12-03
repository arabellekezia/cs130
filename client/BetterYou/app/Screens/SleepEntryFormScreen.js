import React, { useState } from "react";

import { StyleSheet, View } from "react-native";

import Screen from "../components/Screen";
import AppDateTimePicker from "../components/AppDateTimePicker";
import AppText from "../components/AppText";
import TextButton from "../components/TextButton";
import colors from "../config/colors";
import ErrorMessage from "../components/ErrorMessage";
import { ScrollView, Switch } from "react-native-gesture-handler";

import SleepService from "../services/SleepService";

function isValidInput(startDate, endDate, setError) {
  const validStartDate = isValidDate(startDate);
  const validEndDate =
    isValidDate(endDate) && endDate.getTime() > startDate.getTime();
  setError({ startDate: !validStartDate, endDate: !validEndDate });
  return validStartDate && validEndDate;
}

function isValidDate(date) {
  return date instanceof Date && !isNaN(date);
}

function SleepEntryFormScreen({ navigation, route }) {
  const initStartDate = route.params ? new Date(route.params.startTime) : "";
  const initEndDate = route.params ? new Date(route.params.endTime) : "";

  const [startDate, setStartDate] = useState(initStartDate);
  const [endDate, setEndDate] = useState(initEndDate);
  const [isNap, setIsNap] = useState(false);
  const [err, setError] = useState({ startDate: false, endDate: false });

  async function submit() {
    if (!isValidInput(startDate, endDate, setError)) {
      console.log(err);
      return;
    }
    try {
      await SleepService.addSleepEntry(
        Math.floor(startDate.getTime() / 1000),
        Math.floor(endDate.getTime() / 1000),
        isNap
      );
      navigation.popToTop();
    } catch (error) {
      console.log(error);
    }
  }

  function displayErrorMessage(error) {
    if (error.startDate) {
      return <ErrorMessage message="Start date is invalid." />;
    }
    if (error.endDate) {
      return (
        <ErrorMessage message="End date is invalid. Please input a wake time past the sleep time." />
      );
    }
  }

  function toggleSwitch() {
    setIsNap((previousState) => !previousState);
  }

  return (
    <Screen style={styles.container}>
      <ScrollView style={{ padding: 10 }} keyboardShouldPersistTaps="handled">
        <View
          style={{
            backgroundColor: colors.white,
            padding: 10,
            borderColor: "black",
            borderRadius: 10,
            borderWidth: 1,
            flexDirection: "row",
            alignItems: "center",
            marginVertical: 10,
            justifyContent: "space-between",
          }}
        >
          <AppText style={[styles.text, { fontWeight: "bold" }]}>
            Is this a nap?
          </AppText>
          <Switch
            trackColor={{ false: "#767577", true: "#81b0ff" }}
            thumbColor={isNap ? "#f5dd4b" : "#f4f3f4"}
            ios_backgroundColor="#3e3e3e"
            onValueChange={toggleSwitch}
            value={isNap}
          />
        </View>
        <View style={{ padding: 10 }}>
          <AppText style={styles.text}>
            What time did you start sleeping?
          </AppText>
          <AppDateTimePicker
            placeholder="Select a time"
            init={startDate}
            onChange={(date) => {
              setStartDate(date);
              setError({ startDate: false, endDate: false });
            }}
          />
          <AppText style={styles.text}>What time did you wake up?</AppText>
          <AppDateTimePicker
            placeholder="Select a time"
            init={endDate}
            onChange={(date) => {
              setEndDate(date);
              setError({ startDate: false, endDate: false });
            }}
          />
          {displayErrorMessage(err)}
          <TextButton
            style={styles.button}
            name="Submit"
            onPress={async () => {
              await submit();
            }}
          />
        </View>
      </ScrollView>
    </Screen>
  );
}

const styles = StyleSheet.create({
  button: {
    marginVertical: 10,
  },
  container: {
    flex: 1,
    padding: 10,
    justifyContent: "center",
    backgroundColor: colors.background,
  },
  text: {
    fontSize: 16,
  },
});

export default SleepEntryFormScreen;
