import React, { useState } from "react";
import AppText from "./AppText";
import { View, StyleSheet, Text } from "react-native";
import IconButton from "./IconButton";
import moment from "moment";

const StateEnum = Object.freeze({ INITIAL: 0, PAUSED: 1, RUNNING: 2 });

function ElapsedTime({ interval }) {
  const duration = moment.duration(interval);

  function addZeroPadding(duration) {
    return String(duration).padStart(2, "0");
  }

  return (
    <AppText style={styles.elapsedTime}>
      {`${addZeroPadding(duration.hours())}:${addZeroPadding(
        duration.minutes()
      )}:${addZeroPadding(duration.seconds())}`}
    </AppText>
  );
}

function Stopwatch({ onStop }) {
  const [elapsedTime, setElapsedTime] = useState(0);
  const [startTime, setStartTime] = useState(0);
  const [endTime, setEndTime] = useState(0);
  const [timerId, setTimerId] = useState(0);
  const [timerState, setTimerState] = useState(StateEnum.INITIAL);

  function start() {
    setTimerState(StateEnum.RUNNING);
    setTimerId(
      setInterval(() => {
        setElapsedTime((prevTime) => prevTime + 1000);
      }, 1000)
    );
    if (!startTime) {
      setStartTime(Date.now());
    }
  }

  function stop() {
    reset();
    onStop({ elapsedTime, startTime, endTime });
  }

  function pause() {
    setTimerState(StateEnum.PAUSED);
    setEndTime(Date.now());
    clearInterval(timerId);
  }

  function reset() {
    setTimerState(StateEnum.INITIAL);
    clearInterval(timerId);
    setElapsedTime(0);
    setStartTime(0);
  }

  return (
    <View style={styles.container}>
      <ElapsedTime interval={elapsedTime} />
      <View style={styles.buttonsRow}>
        {timerState === StateEnum.PAUSED && (
          <IconButton
            name="restore"
            size={60}
            iconColor="black"
            fontSize={10}
            onPress={() => setElapsedTime(0)}
          />
        )}

        {(timerState === StateEnum.INITIAL ||
          timerState === StateEnum.PAUSED) && (
          <IconButton
            name="play"
            size={60}
            iconColor="white"
            backgroundColor="#3F3DA1"
            fontSize={10}
            border={1}
            onPress={start}
            // style={{ paddingHorizontal: "10%" }}
          />
        )}

        {timerState === StateEnum.RUNNING && (
          <IconButton
            name="pause"
            size={60}
            iconColor="white"
            backgroundColor="#3F3DA1"
            fontSize={10}
            border={1}
            onPress={pause}
            // style={{ paddingHorizontal: "10%" }}
          />
        )}

        {timerState === StateEnum.PAUSED && (
          <IconButton
            name="stop"
            size={60}
            iconColor="black"
            fontSize={10}
            onPress={stop}
          />
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  elapsedTime: {
    fontSize: 76,
    paddingBottom: 14,
    fontWeight: "200",
  },
  buttonsRow: {
    alignSelf: "stretch",
    flexDirection: "row",
    justifyContent: "space-evenly",
    alignItems: "center",
    // backgroundColor: "black",
  },
});
export default Stopwatch;
