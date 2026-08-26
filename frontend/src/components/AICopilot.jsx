import {
  useEffect,
  useRef,
  useState,
} from "react";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";


const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL;


if (!API_BASE_URL) {
  throw new Error(
    "VITE_API_BASE_URL is not configured."
  );
}


const formatCurrency = (
  value,
  currency
) => {

  try {

    return new Intl.NumberFormat(
      "en-IE",
      {
        style: "currency",
        currency: currency,
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      }
    ).format(value);

  } catch {

    return `${Number(value).toFixed(2)} ${currency}`;

  }

};


function AICopilot({
  context,
  onClose,
}) {

  // ==================================================
  // STATE
  // ==================================================

  const [
    messages,
    setMessages,
  ] = useState([]);


  const [
    input,
    setInput,
  ] = useState("");


  const [
    loading,
    setLoading,
  ] = useState(false);


  const [
    error,
    setError,
  ] = useState(null);


  // ==================================================
  // CHAT SCROLL REFERENCE
  // ==================================================

  const chatBottomRef =
    useRef(null);


  // ==================================================
  // AUTOMATIC CHAT SCROLL
  // ==================================================

  useEffect(() => {

    if (
      chatBottomRef.current
    ) {

      chatBottomRef.current.scrollIntoView({
        behavior: "smooth",
        block: "end",
      });

    }

  }, [
    messages,
    loading,
    error,
  ]);


  // ==================================================
  // NO DETECTION SELECTED
  // ==================================================

  if (!context) {

    return null;

  }


  // ==================================================
  // DETECTION CONTEXT
  // ==================================================

  const {
    detection,
    location,
    asset,
  } = context;


  // ==================================================
  // SEND MESSAGE
  // ==================================================

  const sendMessage = async (
    messageText
  ) => {

    const message =
      messageText.trim();


    if (!message) {

      return;

    }


    if (loading) {

      return;

    }


    setError(null);


    // --------------------------------------------------
    // ADD USER MESSAGE
    // --------------------------------------------------

    const userMessage = {

      role: "user",

      content: message,

    };


    setMessages(
      (previousMessages) => [
        ...previousMessages,
        userMessage,
      ]
    );


    // --------------------------------------------------
    // CLEAR INPUT
    // --------------------------------------------------

    setInput("");


    // --------------------------------------------------
    // START LOADING
    // --------------------------------------------------

    setLoading(true);


    try {

      // ================================================
      // CALL FASTAPI
      // ================================================

      const response =
        await fetch(
          `${API_BASE_URL}/api/chat`,
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json",
            },

            body: JSON.stringify({
              detection_id:
                detection.id,

              message:
                message,
            }),

          }
        );


      // ================================================
      // HANDLE HTTP ERROR
      // ================================================

      if (!response.ok) {

        const errorData =
          await response
            .json()
            .catch(
              () => null
            );


        throw new Error(
          errorData?.detail ||
          `AI service returned HTTP ${response.status}`
        );

      }


      // ================================================
      // READ RESPONSE
      // ================================================

      const data =
        await response.json();


      // ================================================
      // ADD AI RESPONSE
      // ================================================

      const assistantMessage = {

        role: "assistant",

        content:
          data.answer || "",

        sources:
          data.sources || [],

        cost:
          data.cost || null,

      };


      setMessages(
        (previousMessages) => [
          ...previousMessages,
          assistantMessage,
        ]
      );


    } catch (err) {

      console.error(
        "Chat API error:",
        err
      );


      setError(
        err.message ||
        "Unable to contact the AI service."
      );


    } finally {

      setLoading(false);

    }

  };


  // ==================================================
  // FORM SUBMIT
  // ==================================================

  const handleSubmit = async (
    event
  ) => {

    event.preventDefault();

    await sendMessage(input);

  };


  // ==================================================
  // SUGGESTIONS
  // ==================================================

  const handleSuggestion =
    async (
      question
    ) => {

      await sendMessage(
        question
      );

    };


  // ==================================================
  // RENDER
  // ==================================================

  return (

    <div className="ai-copilot">


      {/* ==============================================
          HEADER
          ============================================== */}

      <div className="ai-header">

        <div>

          <div className="ai-label">
            AI DECISION COPILOT
          </div>

          <h2>
            {detection.id}
          </h2>

        </div>


        <button
          type="button"
          className="ai-close"
          onClick={onClose}
          aria-label="Close AI Copilot"
        >
          ×
        </button>

      </div>


      {/* ==============================================
          DETECTION CONTEXT
          ============================================== */}

      <div className="ai-context">

        <div className="context-title">
          Current Field Observation
        </div>


        <div className="context-type">
          {detection.type}
        </div>


        <div className="context-row">

          <span>
            Confidence
          </span>

          <strong>
            {
              (
                detection.confidence *
                100
              ).toFixed(0)
            }%
          </strong>

        </div>


        <div className="context-row">

          <span>
            District
          </span>

          <strong>
            {location.district}
          </strong>

        </div>


        <div className="context-row">

          <span>
            Asset
          </span>

          <strong>
            {asset.id}
          </strong>

        </div>

      </div>


      {/* ==============================================
          CHAT AREA
          ============================================== */}

      <div className="ai-chat">


        {/* ============================================
            INITIAL AI MESSAGE
            ============================================ */}

        {messages.length === 0 && (

          <div className="chat-message assistant-message">

            <div className="ai-avatar">
              AI
            </div>


            <div className="assistant-content">

              <div className="ai-bubble">

                <div className="ai-markdown">

                  <p>
                    I understand that you are
                    reviewing{" "}
                    <strong>
                      {detection.type}
                    </strong>{" "}
                    for asset{" "}
                    <strong>
                      {asset.id}
                    </strong>{" "}
                    in{" "}
                    <strong>
                      {location.district}
                    </strong>.
                  </p>


                  <p>
                    I can help you evaluate:
                  </p>


                  <ul>

                    <li>
                      Possible maintenance
                      actions
                    </li>

                    <li>
                      Planned projects
                    </li>

                    <li>
                      Estimated costs
                    </li>

                    <li>
                      Timing
                    </li>

                    <li>
                      Supporting documents
                    </li>

                  </ul>

                </div>

              </div>

            </div>

          </div>

        )}


        {/* ============================================
            CONVERSATION
            ============================================ */}

        {messages.map(
          (
            message,
            index
          ) => (

            <div
              key={index}
              className={
                message.role === "user"
                  ? "chat-message user-message"
                  : "chat-message assistant-message"
              }
            >


              {/* ----------------------------------------
                  ASSISTANT AVATAR
                  ---------------------------------------- */}

              {message.role ===
                "assistant" && (

                <div className="ai-avatar">
                  AI
                </div>

              )}


              {/* ----------------------------------------
                  ASSISTANT CONTENT
                  ---------------------------------------- */}

              {message.role ===
                "assistant" ? (

                <div className="assistant-content">


                  {/* ------------------------------------
                      AI ANSWER
                      ------------------------------------ */}

                  <div className="ai-bubble">

                    <div className="ai-markdown">

                      <ReactMarkdown
                        remarkPlugins={[
                          remarkGfm,
                        ]}
                      >
                        {message.content}
                      </ReactMarkdown>

                    </div>

                  </div>


                  {/* ------------------------------------
                      VERIFIED COST
                      ------------------------------------ */}

                  {message.cost && (

                    <div className="cost-card">

                      <div className="cost-card-header">

                        <span className="cost-check">
                          ✓
                        </span>

                        VERIFIED COST

                      </div>


                      <div className="cost-row">

                        <span>
                          Quantity
                        </span>

                        <strong>
                          {
                            message.cost
                              .quantity
                          }{" "}
                          {
                            message.cost
                              .unit
                          }
                        </strong>

                      </div>


                      <div className="cost-row">

                        <span>
                          Unit Rate
                        </span>

                        <strong>

                          {
                            formatCurrency(
                              message.cost
                                .unit_rate,
                              message.cost
                                .currency
                            )
                          }

                          {" / "}

                          {
                            message.cost
                              .unit
                          }

                        </strong>

                      </div>


                      <div className="cost-total">

                        <span>
                          Estimated Cost
                        </span>

                        <strong>

                          {
                            formatCurrency(
                              message.cost
                                .total_cost,
                              message.cost
                                .currency
                            )
                          }

                        </strong>

                      </div>

                    </div>

                  )}


                  {/* ------------------------------------
                      SUPPORTING DOCUMENTS
                      ------------------------------------ */}

                  {message.sources &&
                    message.sources.length >
                      0 && (

                    <details className="sources-card">

                      <summary>

                        Supporting Documents (
                        {
                          message.sources.length
                        }
                        )

                      </summary>


                      <div className="sources-list">

                        {message.sources.map(
                          (
                            source,
                            sourceIndex
                          ) => (

                            <div
                              key={
                                `${source.document}-${source.folder}`
                              }
                              className="source-item"
                            >

                              <div className="source-number">

                                {
                                  sourceIndex +
                                  1
                                }

                              </div>


                              <div className="source-content">

                                <strong>
                                  {
                                    source.document ||
                                    "Unknown document"
                                  }
                                </strong>


                                <span>
                                  {
                                    source.folder ||
                                    "Folder not specified"
                                  }
                                </span>

                              </div>

                            </div>

                          )
                        )}

                      </div>

                    </details>

                  )}

                </div>

              ) : (

                /* ----------------------------------------
                   USER MESSAGE
                   ---------------------------------------- */

                <div className="user-bubble">

                  {message.content}

                </div>

              )}

            </div>

          )
        )}


        {/* ============================================
            LOADING
            ============================================ */}

        {loading && (

          <div className="chat-message assistant-message">

            <div className="ai-avatar">
              AI
            </div>


            <div className="assistant-content">

              <div className="ai-bubble">

                <div className="thinking-indicator">

                  <span></span>
                  <span></span>
                  <span></span>

                  <span className="thinking-text">
                    Thinking...
                  </span>

                </div>

              </div>

            </div>

          </div>

        )}


        {/* ============================================
            ERROR
            ============================================ */}

        {error && (

          <div className="chat-error">
            {error}
          </div>

        )}


        {/* ============================================
            CHAT BOTTOM ANCHOR
            ============================================ */}

        <div
          ref={chatBottomRef}
          aria-hidden="true"
        />

      </div>


      {/* ==============================================
          SUGGESTIONS
          ============================================== */}

      {messages.length === 0 && (

        <div className="ai-suggestions">

          <button
            type="button"
            onClick={() =>
              handleSuggestion(
                "Should we act now?"
              )
            }
          >
            Should we act now?
          </button>


          <button
            type="button"
            onClick={() =>
              handleSuggestion(
                "Are there planned projects?"
              )
            }
          >
            Are there planned projects?
          </button>


          <button
            type="button"
            onClick={() =>
              handleSuggestion(
                "What could this cost?"
              )
            }
          >
            What could this cost?
          </button>


          <button
            type="button"
            onClick={() =>
              handleSuggestion(
                "What information is missing?"
              )
            }
          >
            What information is missing?
          </button>

        </div>

      )}


      {/* ==============================================
          INPUT
          ============================================== */}

      <form
        className="ai-input-area"
        onSubmit={handleSubmit}
      >

        <input
          type="text"
          value={input}
          onChange={(event) =>
            setInput(
              event.target.value
            )
          }
          placeholder="Ask about this detection..."
          disabled={loading}
        />


        <button
          type="submit"
          disabled={
            loading ||
            !input.trim()
          }
        >
          {loading
            ? "..."
            : "Send"}
        </button>

      </form>

    </div>

  );

}


export default AICopilot;