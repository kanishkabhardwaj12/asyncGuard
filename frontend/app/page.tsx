export default function HomePage() {
    return (
      <>
        <div className="scanline-bg" />
        <div className="vignette" />
  
        <main className="container">
          <div className="hud-bar">
            <span>Home // 2025</span>
            <div className="icons">
              <span>[Globe]</span>
              <span>[Flag]</span>
              <span>[Mute]</span>
            </div>
          </div>
  
          <h1>CHECKPOINT</h1>
          <p className="subtitle">Look back at your 2025 on Discord</p>
  
          <form className="login-form">
            <div className="input-wrapper">
              <label>IDENTIFIER</label>
              <input type="text" placeholder="user@discord.com" />
            </div>
  
            <div className="input-wrapper">
              <label>KEY</label>
              <input type="password" placeholder="••••••••" />
            </div>
  
            <button type="button" className="start-btn">
              <span>▶</span> Start
            </button>
          </form>
  
          <div className="footer-text">
            Only you can see your Checkpoint.{" "}
            <a href="#">Learn More.</a>
          </div>
  
          <div className="wumpus-badge">
            WUMP<br />
            CONTENT RATED BY<br />
            DISCORD
          </div>
        </main>
      </>
    );
  }
  