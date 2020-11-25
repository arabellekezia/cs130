import React, { useState } from "react";

import { StyleSheet, View } from "react-native";

import Screen from "../components/Screen";
import AppDateTimePicker from "../components/AppDateTimePicker";
import AppText from "../components/AppText";
import TextButton from "../components/TextButton";
import colors from "../config/colors";

function SleepEntryFormScreen(props) {
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  return (
    <Screen style={styles.container}>
      <View style={{ padding: 10 }}>
        <AppText style={styles.text}>What time did you start sleeping?</AppText>
        <AppDateTimePicker
          placeholder="Select a time"
          onChange={(date) => {
            setStartDate(date);
          }}
        />
        <AppText style={styles.text}>What time did you wake up?</AppText>
        <AppDateTimePicker
          placeholder="Select a time"
          onChange={(date) => {
            setEndDate(date);
          }}
        />
        <TextButton
          name="Submit"
          onPress={() => {
            console.log("start: " + startDate.toLocaleString());
            console.log("end: " + endDate.toLocaleString());
          }}
        />
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 10,
    justifyContent: "center",
    backgroundColor: colors.primary,
  },
  text: {
    fontSize: 16,
  },
});

export default SleepEntryFormScreen;
