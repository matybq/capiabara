// Capibara — usa la imagen PNG de referencia con overlays de accesorios
// La imagen ya incluye el mate, así que el mate no es un accesorio opcional sino parte del personaje.
// Accesorios se superponen como SVG encima.
function Capybara({
  accessory = 'none',
  // eslint-disable-next-line no-unused-vars
  mood = 'chill',
  size = 220,
  animated = true,
  talking = false,
}) {
  const breathe = animated ? 'capy-breathe' : '';
  const talk    = talking ? 'capy-talking' : '';

  return (
    <div
      className={`capybara-wrap ${breathe} ${talk}`}
      style={{
        width: size,
        height: size,
        display: 'inline-block',
        position: 'relative',
        userSelect: 'none',
      }}
    >
      {/* Imagen base */}
      <img
        src="assets/capi.png"
        alt="Capibara"
        draggable={false}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'contain',
          display: 'block',
          pointerEvents: 'none',
        }}
      />

      {/* Overlays de accesorios — posicionados en % sobre la imagen */}
      {accessory === 'sunglasses' && (
        <svg
          viewBox="0 0 100 100"
          style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', pointerEvents: 'none' }}
        >
          {/* Lente derecho (ojo de la capi) */}
          <g transform="translate(38 16)">
            <rect x="0" y="0" width="16" height="11" rx="2.5" fill="#1a1a1a" stroke="#000" strokeWidth="0.8"/>
            <rect x="18" y="0" width="16" height="11" rx="2.5" fill="#1a1a1a" stroke="#000" strokeWidth="0.8"/>
            <line x1="16" y1="5" x2="18" y2="5" stroke="#000" strokeWidth="0.8"/>
            {/* highlight */}
            <rect x="2" y="2" width="5" height="2" rx="1" fill="#fff" opacity="0.35"/>
            <rect x="20" y="2" width="5" height="2" rx="1" fill="#fff" opacity="0.35"/>
          </g>
        </svg>
      )}

      {accessory === 'sleep' && (
        <svg
          viewBox="0 0 100 100"
          style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', pointerEvents: 'none' }}
        >
          <g className="capy-zzz" fontFamily="'Fraunces', serif" fontWeight="700" fill="#3A2418">
            <text x="70" y="22" fontSize="8">z</text>
            <text x="76" y="15" fontSize="10">z</text>
            <text x="84" y="7"  fontSize="12">Z</text>
          </g>
        </svg>
      )}

      {accessory === 'birra' && (
        <svg
          viewBox="0 0 100 100"
          style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', pointerEvents: 'none' }}
        >
          {/* Latita a la derecha de la capi */}
          <g transform="translate(82 60)">
            <rect x="0" y="0" width="10" height="22" rx="1.5" fill="#2D4A1F" stroke="#1a1a1a" strokeWidth="0.6"/>
            <rect x="0" y="8" width="10" height="7" fill="#F5E6A8"/>
            <rect x="3" y="-2" width="4" height="2.5" rx="0.5" fill="#2D4A1F" stroke="#1a1a1a" strokeWidth="0.5"/>
          </g>
        </svg>
      )}

      {accessory === 'heart' && (
        <svg
          viewBox="0 0 100 100"
          style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', pointerEvents: 'none' }}
        >
          <g className="capy-hearts" fill="#E85A7C">
            <path className="capy-heart1" d="M 72 18 q -4 -5 -8 0 q -4 5 0 10 q 4 4 8 8 q 4 -4 8 -8 q 4 -5 0 -10 q -4 -5 -8 0 Z" transform="scale(0.5) translate(72 18)"/>
          </g>
        </svg>
      )}

      <style>{`
        .capybara-wrap img { -webkit-user-drag: none; }
        .capy-breathe img {
          animation: capyBreathe 3.8s ease-in-out infinite;
          transform-origin: 50% 90%;
        }
        .capy-talking img {
          animation: capyTalk 0.35s ease-in-out infinite !important;
          transform-origin: 50% 90%;
        }
        .capy-zzz text {
          animation: capyZzz 2.8s ease-in-out infinite;
          transform-box: fill-box;
          transform-origin: center;
          opacity: 0;
        }
        .capy-zzz text:nth-child(1) { animation-delay: 0s;   }
        .capy-zzz text:nth-child(2) { animation-delay: 0.4s; }
        .capy-zzz text:nth-child(3) { animation-delay: 0.8s; }

        .capy-hearts .capy-heart1 {
          animation: capyHeart 2s ease-in-out infinite;
          transform-box: fill-box;
          transform-origin: center;
        }

        @keyframes capyBreathe {
          0%, 100% { transform: scale(1); }
          50%      { transform: scale(1.015); }
        }
        @keyframes capyTalk {
          0%, 100% { transform: translateY(0) scale(1); }
          50%      { transform: translateY(-1.5px) scale(1.01); }
        }
        @keyframes capyZzz {
          0%, 100% { opacity: 0; transform: translateY(3px); }
          40%, 70% { opacity: 1; transform: translateY(-3px); }
        }
        @keyframes capyHeart {
          0%   { opacity: 0; transform: translateY(0) scale(0.6); }
          30%  { opacity: 1; transform: translateY(-4px) scale(1); }
          100% { opacity: 0; transform: translateY(-12px) scale(0.8); }
        }
      `}</style>
    </div>
  );
}

export default Capybara;
