import React, { useState } from "react";
import axios from "axios";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css"; 
import "./RuleEvaluator.css";

const RuleEvaluator = () => {
  const [rule, setRule] = useState("");
  const [evaluationData, setEvaluationData] = useState("");
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const dataToEvaluate = JSON.parse(evaluationData);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/evaluate_rule/",
        {
          rule: rule,
          data: dataToEvaluate,
        }
      );

      const evaluationResult = response.data.result;
      setResult(evaluationResult);

      if (evaluationResult) {
        toast.success("Evaluation Result: True");
      } else {
        toast.error("Evaluation Result: False");
      }
    } catch (error) {
      console.error("Error evaluating rule:", error);
      setResult(null);
      toast.error("Error evaluating rule.");
    }
  };

  return (
    <div className="container">
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <label htmlFor="rule-input">Rule:</label>
          <input
            id="rule-input"
            type="text"
            value={rule}
            onChange={(e) => setRule(e.target.value)}
            required
          />
        </div>
        <div className="input-group">
          <label htmlFor="evaluation-data">Evaluation Data (JSON):</label>
          <textarea
            id="evaluation-data"
            value={evaluationData}
            onChange={(e) => setEvaluationData(e.target.value)}
            required
          />
        </div>
        <button type="submit">Evaluate</button>
      </form>
      <ToastContainer position="top-center" autoClose={3000} />
    </div>
  );
};

export default RuleEvaluator;
