export const millisecondTimeStampToSeconds = (timestamp) => {
  return Math.floor(timestamp / 1000);
};

export const roundToOne = (num) => {
  return +(Math.round(num + "e+1") + "e-1");
};
