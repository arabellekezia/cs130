import React, { useState } from "react";

import { StyleSheet, View } from "react-native";

import Screen from "../components/Screen";
import AppDateTimePicker from "../components/AppDateTimePicker";
import AppText from "../components/AppText";
import TextButton from "../components/TextButton";
import colors from "../config/colors";
import ErrorMessage from "../components/ErrorMessage";
import { ScrollView } from "react-native-gesture-handler";

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
  const [err, setError] = useState({ startDate: false, endDate: false });

  function submit() {
    if (!isValidInput(startDate, endDate, setError)) {
      console.log(err);
      return;
    }
    console.log("start: " + startDate.toLocaleString());
    console.log("end: " + endDate.toLocaleString());
    navigation.popToTop();
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

  return (
    <Screen style={styles.container}>
      <ScrollView style={{ padding: 10 }} keyboardShouldPersistTaps="handled">
        <AppText style={styles.text}>What time did you start sleeping?</AppText>
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
          name="Submit"
          onPress={() => {
            submit();
          }}
        />
      </ScrollView>
    </Screen>
  );
}

const styles = StyleSheet.create({
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
