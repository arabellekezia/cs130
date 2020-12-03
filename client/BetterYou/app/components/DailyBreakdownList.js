import React from "react";
import { StyleSheet, View } from "react-native";
import { useNavigation } from "@react-navigation/native";
import ListItemComponent from "./ListItemComponent";

import moment from "moment";

function DailyBreakdownList({ style, entries, type }) {
  const daysOfWeek = {
    Sunday: 0,
    Monday: 1,
    Tuesday: 2,
    Wednesday: 3,
    Thursday: 4,
    Friday: 5,
    Saturday: 6,
  };

  const navigation = useNavigation();
  return (
    <View style={{ ...styles.container, ...style }}>
      {entries.map((entry, key) => {
        const { title, icon, description } = entry;
        return (
          <ListItemComponent
            key={key}
            title={title}
            icon={icon}
            description={description}
            onPress={() => {
              const weekStart = moment().startOf("week");
              const date = moment(weekStart)
                .add(daysOfWeek[title], "days")
                .valueOf();
              navigation.navigate(type, { date: date });
            }}
          />
        );
      })}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    justifyContent: "center",
    alignItems: "flex-start",
    width: "100%",
  },
});

export default DailyBreakdownList;
