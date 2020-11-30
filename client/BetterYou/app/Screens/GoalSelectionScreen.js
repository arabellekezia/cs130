import React from "react";
import { SafeAreaView, StyleSheet, View } from "react-native";
import IconButton from "../components/IconButton";
import TitleText from "../components/TitleText";

function GoalSelectionScreen({ navigation }) {
  return (
    <SafeAreaView style={styles.container}>
      <TitleText style={styles.header} children="Goals" />
      <View style={styles.rowSelection}>
        <IconButton
          style={styles.button}
          name="food-apple"
          size={74}
          iconColor="#7e7e7e"
          label="Diet"
          border={2}
          onPress={() => navigation.navigate("DietGoals")}
        />
        <IconButton
          style={styles.button}
          name="dumbbell"
          size={74}
          iconColor="#7e7e7e"
          label="Fitness"
          border={2}
          onPress={() => navigation.navigate("FitnessGoals")}
        />
        <IconButton
          style={styles.button}
          name="sleep"
          size={74}
          iconColor="#7e7e7e"
          label="Sleep"
          border={2}
          onPress={() => navigation.navigate("SleepGoals")}
        />
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "white",
    alignItems: "center",
    justifyContent: "center",
  },
  rowSelection: {
    flex: 1,
    width: "100%",
    flexDirection: "row",
    justifyContent: "space-around",
    alignItems: "center",
  },
  header: {
    alignSelf: "flex-start",
    marginTop: "10%",
    marginLeft: "5%",
  },
});

export default GoalSelectionScreen;
