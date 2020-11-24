import React from "react";

import { View, StyleSheet } from "react-native";

import colors from "../config/colors";

import HeaderText from "../components/HeaderText";
import IconButton from "../components/IconButton";
import Screen from "../components/Screen";

function DietGoalEntryTypeSelectScreen(props) {
  return (
    <Screen style={styles.container}>
      <HeaderText style={{ marginBottom: 50 }}>
        Select an input method
      </HeaderText>
      <View style={styles.buttonContainer}>
        <IconButton
          name="barcode"
          size={60}
          label="Scan barcode"
          iconColor={colors.dark}
          border={2}
          onPress={() => console.log("navigate to barcode scan screen ")}
        />
        <IconButton
          name="database-search"
          size={60}
          label="Look up"
          iconColor={colors.dark}
          border={2}
          onPress={() => console.log("navigate to lookup screen")}
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

export default DietGoalEntryTypeSelectScreen;
