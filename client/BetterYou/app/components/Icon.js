import React from "react";
import { View, StyleSheet } from "react-native";
import { MaterialCommunityIcons } from "@expo/vector-icons";

function Icon({
  name,
  size,
  backgroundColor = "black",
  iconColor = "white",
  iconScale = 0.6,
}) {
  return (
    <View
      style={[
        { width: size, height: size, borderRadius: size / 2, backgroundColor },
        styles.iconContainer,
      ]}
    >
      <MaterialCommunityIcons
        name={name}
        color={iconColor}
        size={size * iconScale}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  iconContainer: {
    justifyContent: "center",
    alignItems: "center",
  },
});

export default Icon;
