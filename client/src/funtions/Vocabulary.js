export const vocabC = async (data) => {
  return await axios.post(import.meta.env.VITE_API_URL + "/Vocabulary", data, )
};
