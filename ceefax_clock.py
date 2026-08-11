"""Clock helper for the Ceefax dashboard."""


def get_clock_script() -> str:
    """Return the JavaScript for the teletext clock updater."""
    return """
    <script>
    (function() {
        const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        const clock = document.getElementById('ceefax-time');
        if (!clock) return;
        function updateTime() {
            const now = new Date();
            const formatted = `${days[now.getDay()]} ${String(now.getDate()).padStart(2, '0')} ${months[now.getMonth()]} ${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`;
            clock.textContent = formatted;
        }
        updateTime();
        setInterval(updateTime, 1000);
    })();
    </script>
    """
