import React from "react";

import { View, StyleSheet } from "react-native";

import colors from "../config/colors";
import HeaderText from "../components/HeaderText";
import IconButton from "../components/IconButton";
import Screen from "../components/Screen";

function EntryCategorySelectScreen(props) {
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
          onPress={() => console.log("navigate to sleep entry screen")}
        />
        <IconButton
          name="food-apple"
          size={60}
          label="Diet"
          iconColor={colors.diet}
          border={2}
          onPress={() => console.log("navigate to diet entry screen")}
        />
        <IconButton
          name="google-fit"
          size={60}
          label="Fitness"
          iconColor={colors.fitness}
          border={2}
          onPress={() => console.log("navigate to fitness entry screen")}
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
    backgroundColor: colors.primary,
  },
});

export default EntryCategorySelectScreen;
