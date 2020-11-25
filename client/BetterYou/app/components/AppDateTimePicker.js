import React, { useState } from "react";
import { View, StyleSheet } from "react-native";

import colors from "../config/colors";
import AppText from "./AppText";
import DateTimePickerModal from "react-native-modal-datetime-picker";
import Screen from "./Screen";
import { TouchableWithoutFeedback } from "react-native-gesture-handler";
import { MaterialCommunityIcons } from "@expo/vector-icons";

function AppDateTimePicker({ placeholder }) {
  const [date, setDate] = useState("");
  const [isDatePickerVisible, setDatePickerVisibility] = useState(false);
  const [isTimePickerVisible, setTimePickerVisibility] = useState(false);
  const [isCanceled, setCanceled] = useState(false);

  const showDatePicker = () => {
    setDatePickerVisibility(true);
  };

  const showTimePicker = () => {
    setTimePickerVisibility(true);
  };

  const hideDatePicker = () => {
    setDatePickerVisibility(false);
  };

  const hideTimePicker = () => {
    setTimePickerVisibility(false);
  };

  const handleDateConfirm = (selectedDate) => {
    setDate(selectedDate);
    hideDatePicker();
  };

  const handleTimeConfirm = (selectedTime) => {
    date.setHours(selectedTime.getHours(), selectedTime.getMinutes(), 0);
    console.log(date.toLocaleString());
    setDate(date);
    hideTimePicker();
  };

  return (
    <Screen>
      <TouchableWithoutFeedback
        style={{ ...styles.container }}
        onPress={() => {
          showDatePicker();
          setCanceled(false);
        }}
      >
        <MaterialCommunityIcons
          name="calendar-clock"
          color={colors.medium}
          size={26}
          style={styles.icon}
        />
        {date ? (
          <AppText style={styles.text}>
            {date.toLocaleString("en-US", {
              year: "numeric",
              month: "short",
              day: "numeric",
              hour: "numeric",
              minute: "numeric",
              hour12: true,
            })}
          </AppText>
        ) : (
          <AppText style={styles.placeholder}>{placeholder}</AppText>
        )}
        <MaterialCommunityIcons
          name="chevron-down"
          color={colors.medium}
          size={26}
        />
      </TouchableWithoutFeedback>

      <DateTimePickerModal
        isVisible={isDatePickerVisible}
        mode="date"
        onConfirm={handleDateConfirm}
        onCancel={() => {
          setCanceled(true);
          hideDatePicker();
        }}
        onHide={() => {
          if (!isCanceled) {
            showTimePicker();
          }
        }}
      />
      <DateTimePickerModal
        headerTextIOS="Pick a time"
        isVisible={isTimePickerVisible}
        mode="time"
        onConfirm={handleTimeConfirm}
        onCancel={hideTimePicker}
      />
    </Screen>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: colors.light,
    borderRadius: 10,
    width: "100%",
    flexDirection: "row",
    padding: 15,
    marginVertical: 10,
  },
  icon: {
    marginRight: 14,
  },
  placeholder: {
    flex: 1,
    fontSize: 18,
    color: colors.medium,
  },
  text: {
    flex: 1,
    fontSize: 18,
    color: colors.dark,
  },
});

export default AppDateTimePicker;
