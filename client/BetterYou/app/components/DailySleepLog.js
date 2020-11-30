import React from 'react';
import { StyleSheet, View } from 'react-native';

import SleepEntry from './SleepEntry';

function DailySleepLog({ style, entries }) {
  return (
    <View style={{ ...styles.container, ...style }}>
      {entries.map((entry, key) => {
        const {
          sleeptime,
          waketime,
        } = entry;
        return (
          <SleepEntry
            key={key}
            style={styles.entry}
            sleeptime={sleeptime}
            waketime={waketime}
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
})

export default DailySleepLog;