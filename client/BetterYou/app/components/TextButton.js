import React from "react";

import { Platform, StyleSheet, TouchableOpacity, View } from "react-native";
import AppText from "./AppText";

function TextButton({
  onPress,
  name,
  textColor = "white",
  fontSize = 17,
  fontWeight = "600",
  style,
}) {
  return (
    <TouchableOpacity onPress={onPress} activeOpacity={0.7}>
      <View style={{ ...styles.container, ...style }}>
        <AppText
          style={{
            color: textColor,
            fontSize,
            fontWeight,
          }}
        >
          {name}
        </AppText>
      </View>
    </TouchableOpacity>
  );
}

function getDefaultBackgroundColor() {
  const defaultAndroidBackgroundColor = "#2196F3";
  const defaultIOSBackgroundColor = "#007AFF";

  return Platform.OS === "android"
    ? defaultAndroidBackgroundColor
    : defaultIOSBackgroundColor;
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: getDefaultBackgroundColor(),
    alignItems: "center",
    justifyContent: "center",
    paddingVertical: 10,
    paddingHorizontal: 30,
    borderRadius: 10,
    minWidth: 110,
  },
});

export default TextButton;
