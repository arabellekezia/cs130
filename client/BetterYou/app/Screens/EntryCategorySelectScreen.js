import React from "react";

import { View, StyleSheet } from "react-native";

import colors from "../config/colors";
import HeaderText from "../components/HeaderText";
import IconButton from "../components/IconButton";
import Screen from "../components/Screen";

function EntryCategorySelectScreen({ navigation }) {
  return (
    <Screen style={styles.container}>
      <HeaderText>Select a category</HeaderText>
      <View style={styles.buttonContainer}>
        <IconButton
          name="sleep"
          size={60}
          label="Sleep"
          iconColor={colors.sleep}
          border={2}
          onPress={() => navigation.navigate("SleepGoalEntryTypeSelect")}
        />
        <IconButton
          name="food-apple"
          size={60}
          label="Nutrition"
          iconColor={colors.diet}
          border={2}
          onPress={() => navigation.navigate("DietGoalEntryTypeSelect")}
        />
        <IconButton
          name="google-fit"
          size={60}
          label="Fitness"
          iconColor={colors.fitness}
          border={2}
          onPress={() => navigation.navigate("FitnessGoalEntryTypeSelect")}
        />
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  buttonContainer: {
    marginVertical: 40,
    alignSelf: "stretch",
    flexDirection: "row",
    justifyContent: "space-evenly",
  },
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: colors.background,
  },
});

export default EntryCategorySelectScreen;
