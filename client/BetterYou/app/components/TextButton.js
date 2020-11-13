import React from "react";

import { Platform, Text, TouchableOpacity, View } from "react-native";
import AppText from "./AppText";

function TextButton({
  onPress,
  name,
  textColor = "white",
  fontSize = 17,
  fontWeight = "600",
  backgroundColor = getDefaultBackgroundColor(),
  minWidth = 110,
  borderRadius = 10,
}) {
  return (
    <TouchableOpacity activeOpacity={0.6} onPress={onPress}>
      <View
        style={{
          backgroundColor,
          alignItems: "center",
          justifyContent: "center",
          paddingVertical: 10,
          paddingHorizontal: 30,
          borderRadius,
          minWidth,
        }}
      >
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

export default TextButton;
