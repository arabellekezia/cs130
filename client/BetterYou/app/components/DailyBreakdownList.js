import React from 'react';
import { StyleSheet, View } from 'react-native';


//import AppText from './AppText';
import ListItemComponent from './ListItemComponent';

function DailyBreakdownList({ style, entries }) {
  return (
    <View style={{ ...styles.container, ...style }}>
      {entries.map((entry, key) => {
        const {
          title, 
          icon, 
          description, 
          navigation, 
          destination
        } = entry;
        return (
          <ListItemComponent
            key={key}
            title={title}
            icon={icon}
            description={description}
            navigation={navigation}
            destination={destination}
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