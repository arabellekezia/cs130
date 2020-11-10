import React from "react";
import { View, StyleSheet } from "react-native";
import { MaterialCommunityIcons } from "@expo/vector-icons";

function Icon({
  name,
  size,
  backgroundColor = "black",
  iconColor = "white",
  iconScale = 0.5,
  border,
}) {
  return (
    <View
      style={[
        {
          width: size,
          height: size,
          borderRadius: size / 2,
          backgroundColor,
          borderWidth: border, // 1 if border is provided, 0 otherwise
          borderColor: iconColor,
        },
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
