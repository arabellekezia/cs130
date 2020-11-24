import React from "react";

import { View, StyleSheet } from "react-native";

import colors from "../config/colors";

import HeaderText from "../components/HeaderText";
import IconButton from "../components/IconButton";
import Screen from "../components/Screen";

function SleepGoalEntryTypeSelectScreen(props) {
  return (
    <Screen style={styles.container}>
      <HeaderText style={{ marginBottom: 50 }}>
        Select an input method
      </HeaderText>
      <View style={styles.buttonContainer}>
        <IconButton
          name="timer"
          size={60}
          label="Start timer"
          iconColor={colors.dark}
          border={2}
          onPress={() => console.log("navigate to timer screen ")}
        />
        <IconButton
          name="fountain-pen-tip"
          size={60}
          label="Manual input"
          iconColor={colors.dark}
          border={2}
          onPress={() => console.log("navigate to manual input screen")}
        />
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  buttonContainer: {
    alignSelf: "stretch",
    flexDirection: "row",
    justifyContent: "space-evenly",
  },
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: colors.primary,
  },
});

export default SleepGoalEntryTypeSelectScreen;
