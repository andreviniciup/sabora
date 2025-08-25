import React, { useEffect, useState } from 'react';

const ErrorNotification = ({ error, onClose }) => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    if (error) {
      setIsVisible(true);
      // Auto-hide after 5 seconds
      const timer = setTimeout(() => {
        setIsVisible(false);
        setTimeout(() => onClose(), 300); // Wait for animation to complete
      }, 5000);

      return () => clearTimeout(timer);
    }
  }, [error, onClose]);

  if (!error || !isVisible) return null;

  return (
    <div className="fixed top-4 left-4 z-50 animate-fade-in">
      <div 
        data-layer="Frame 38" 
        className="Frame38 px-[59px] py-[30px] bg-red-900/75 rounded-[25px] shadow-[0px_0px_8px_3px_rgba(122,57,57,0.25)] outline outline-1 outline-offset-[-1px] inline-flex justify-start items-center gap-2.5"
      >
        <div 
          data-layer="Error: mensagem do erro" 
          className="ErrorMensagemDoErro text-center justify-start"
        >
          <span className="text-white text-xl font-medium font-['Alexandria'] leading-[23px]">
            Error: 
          </span>
          <span className="text-white text-base font-normal font-['Alexandria'] leading-[23px] ml-1">
            {error}
          </span>
        </div>
        <button
          onClick={() => {
            setIsVisible(false);
            setTimeout(() => onClose(), 300);
          }}
          className="ml-2 text-white hover:text-red-200 transition-colors"
        >
          ✕
        </button>
      </div>
    </div>
  );
};

export default ErrorNotification;
