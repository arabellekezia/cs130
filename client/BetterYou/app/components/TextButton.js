import React from "react";

import { Platform, Text, TouchableOpacity, View } from "react-native";

function TextButton({
  onPress,
  name,
  textColor = "white",
  fontSize = 17,
  fontWeight = "600",
  backgroundColor = getDefaultBackgroundColor(),
  minWidth = 110,
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
          borderRadius: 10,
          minWidth,
        }}
      >
        <Text
          style={{
            color: textColor,
            fontSize,
            fontWeight,
          }}
        >
          {name}
        </Text>
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
