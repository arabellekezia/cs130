import React from "react";

import { TextInput, View, StyleSheet } from "react-native";

import { MaterialCommunityIcons } from "@expo/vector-icons";

function AppTextInput({ icon, ...kwargs }) {
  return (
    <View style={styles.container}>
      {icon && (
        <MaterialCommunityIcons
          name={icon}
          color="#7e7e7e"
          size={20}
          style={styles.icon}
        />
      )}
      <TextInput {...kwargs} style={styles.textInput} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: "#efefef",
    borderRadius: 10,
    width: "100%",
    flexDirection: "row",
    padding: 15,
    marginVertical: 10,
  },
  icon: {
    marginRight: 10,
  },

  textInput: {
    fontSize: 16,
  },
});
export default AppTextInput;
