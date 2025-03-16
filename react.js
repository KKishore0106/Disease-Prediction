import React, { useState } from "react";
import axios from "axios";
import { useForm } from "react-hook-form";

export default function Home() {
  const { register, handleSubmit } = useForm();
  const [result, setResult] = useState(null);
  const [suggestion, setSuggestion] = useState(null);

  const onSubmit = async (data) => {
    try {
      const response = await axios.post("https://your-backend-url/predict", data);
      setResult(response.data.prediction);
      setSuggestion(response.data.suggestion);
    } catch (error) {
      console.error("Error predicting disease:", error);
    }
  };

  return (
    <div className="container mx-auto p-8">
      <h1 className="text-3xl font-bold text-center mb-6">Disease Prediction System</h1>
      <form onSubmit={handleSubmit(onSubmit)} className="bg-white shadow-md p-6 rounded-lg">
        <label className="block mb-2">Glucose Level</label>
        <input className="border p-2 w-full" {...register("glucose", { required: true })} />

        <label className="block mt-4 mb-2">Blood Pressure</label>
        <input className="border p-2 w-full" {...register("blood_pressure", { required: true })} />

        <button type="submit" className="mt-6 bg-blue-500 text-white py-2 px-4 rounded">Predict</button>
      </form>
      {result && (
        <div className="mt-6 p-4 bg-green-100 border border-green-500 rounded">
          <h2 className="text-xl font-bold">Prediction Result</h2>
          <p>{result}</p>
          <h3 className="text-lg mt-4">AI Suggestion:</h3>
          <p>{suggestion}</p>
        </div>
      )}
    </div>
  );
}
