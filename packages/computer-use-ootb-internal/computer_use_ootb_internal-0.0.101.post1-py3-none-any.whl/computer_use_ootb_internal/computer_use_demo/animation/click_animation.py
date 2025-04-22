"""
show_click(x, y, duration_ms=800)
 → 在屏幕 (x,y) 显示点击动画，停留 duration_ms 毫秒
依赖: pyside6
确保同目录有 click.gif
"""
import sys, time
from pathlib import Path
from PySide6.QtCore import Qt, QPoint, QTimer, QEventLoop, QSize, QEasingCurve, QPropertyAnimation
from PySide6.QtGui  import QPainter, QPixmap, QMovie
from PySide6.QtWidgets import QApplication, QWidget, QLabel

CLICK_GIF = Path(__file__).with_name("icons8-select-cursor-transparent-96.gif")

class ClickAnimation(QWidget):
    def __init__(self, pos: QPoint, life_ms: int):
        super().__init__(None,
            Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint
            | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        if not CLICK_GIF.exists():
            print(f"Error: click.gif not found at {CLICK_GIF}")
            return
            
        try:
            # 创建标签显示GIF
            self.label = QLabel(self)
            self.movie = QMovie(str(CLICK_GIF))
            
            # 获取原始尺寸并打印（仅供参考）
            self.movie.jumpToFrame(0)
            original_size = self.movie.currentPixmap().size()
            print(f"GIF original size: {original_size.width()}x{original_size.height()}")
            
            # 将GIF缩放到30x30像素
            target_size = QSize(50, 50)
            self.movie.setScaledSize(target_size)
            
            # 设置标签尺寸和GIF
            self.label.setMovie(self.movie)
            self.label.setFixedSize(target_size)
            
            # 设置窗口大小和位置
            self.resize(target_size)
            self.move(pos.x() - 15, pos.y() - 15)  # 居中显示
            
            # 提高播放性能
            self.movie.setCacheMode(QMovie.CacheAll)
            
            # 开始播放动画
            self.movie.start()
            
            # 设置定时器关闭窗口
            QTimer.singleShot(life_ms, self.close)
            
            self.show()
            self.raise_()
            print(f"Click animation created at ({pos.x()}, {pos.y()}), size: 30x30, duration: {life_ms}ms")
        except Exception as e:
            print(f"Error creating click animation: {str(e)}")

# ---------- 外部接口 ----------
_app = None
def _ensure_app():
    global _app
    if _app is None:
        if QApplication.instance() is None:
            print("Creating new QApplication instance")
            _app = QApplication(sys.argv)
        else:
            print("Using existing QApplication instance")
            _app = QApplication.instance()

# Keep references to animations to prevent garbage collection
_active_animations = []

def show_click(x: int, y: int, duration_ms: int = 2000, existing_ms: int = 2000):  # 增加默认播放时间和静止时间
    """非阻塞式点击动画：立即返回，动画在后台运行
    
    Args:
        x, y          : 屏幕坐标
        duration_ms   : 动画播放时长
        existing_ms   : 动画结束后静止显示的时间
    """
    print(f"Attempting to show click at ({x}, {y})")
    
    if not CLICK_GIF.exists():
        raise FileNotFoundError(f"click.gif not found at {CLICK_GIF}")
        
    _ensure_app()
    
    try:
        # 总生存时间 = 动画时间 + 静止显示时间
        total_life_ms = duration_ms + existing_ms
        animation = ClickAnimation(QPoint(x, y), total_life_ms)
        
        # Store reference to prevent garbage collection
        global _active_animations
        _active_animations.append(animation)
        
        # Set up cleanup after animation completes + existing time
        QTimer.singleShot(total_life_ms + 150, lambda: _clean_animation(animation))
        
        print(f"Click animation started (non-blocking, will exist for {total_life_ms}ms)")
    except Exception as e:
        print(f"Error during show_click: {str(e)}")


def _clean_animation(animation):
    """Remove animation from reference list after it completes"""
    global _active_animations
    if animation in _active_animations:
        _active_animations.remove(animation)
    print("Animation cleaned up")


# ---------- 新增函数 ----------
def show_move_to(x1: int, y1: int, x2: int, y2: int, duration_ms: int = 1000, existing_ms: int = 3000):
    """
    非阻塞式移动动画：在 (x1, y1) 处出现光标 GIF，
    并在 duration_ms 毫秒内平滑移动到 (x2, y2)，
    然后在终点静止显示 existing_ms 毫秒。
    立即返回，动画在后台运行。

    Args:
        x1, y1        : 起点屏幕坐标
        x2, y2        : 终点屏幕坐标
        duration_ms   : 移动总时长
        existing_ms   : 移动结束后在终点静止显示的时间
    """
    print(f"Attempting to move click from ({x1}, {y1}) → ({x2}, {y2}) "
          f"in {duration_ms} ms, then stay for {existing_ms} ms")

    if not CLICK_GIF.exists():
        raise FileNotFoundError(f"click.gif not found at {CLICK_GIF}")

    _ensure_app()

    # 总生存时间 = 动画时间 + 静止显示时间
    total_life_ms = duration_ms + existing_ms
    widget = ClickAnimation(QPoint(x1, y1), total_life_ms)
    
    # 用 QPropertyAnimation 平滑移动窗口
    anim = QPropertyAnimation(widget, b"pos")
    anim.setDuration(duration_ms)
    # ClickAnimation 内部已经向左上偏移了 15px，这里沿用同样的偏移
    anim.setStartValue(QPoint(x1 - 15, y1 - 15))
    anim.setEndValue(QPoint(x2 - 15, y2 - 15))
    anim.setEasingCurve(QEasingCurve.OutQuad)     # 可自行更换缓动曲线
    
    # Store references to both widget and animation to prevent garbage collection
    global _active_animations
    # Store them as a tuple to keep both references
    animation_pair = (widget, anim)
    _active_animations.append(animation_pair)
    
    # Clean up both widget and animation after completion of total life time
    def cleanup():
        if animation_pair in _active_animations:
            _active_animations.remove(animation_pair)
        print("Move animation cleaned up")
    
    # Connect finished signal only to print a message
    anim.finished.connect(lambda: print("Movement finished, now staying still"))
    
    # Start the animation
    anim.start()
    
    # Process events immediately to kickstart the animation
    QApplication.processEvents()
    
    # Set up final cleanup after animation + existing time
    QTimer.singleShot(total_life_ms, cleanup)
    
    print("Move-to animation started (non-blocking)")


# ---------- 命令行测试 ----------
if __name__ == "__main__":
    # 确保应用程序实例存在
    _ensure_app()
    
    # 测试点击
    print("Testing non-blocking click animation...")
    x, y = 500, 500
    show_click(x, y)
    
    # 测试同时运行两个动画
    print("\nTesting simultaneous animations...")
    x1, y1 = 200, 200
    x2, y2 = 600, 600
    # show_click(x1, y1)
    show_move_to(x1, y1, x2, y2, duration_ms=2000)
    
    # # 测试先移动，然后点击
    print("\nTesting sequence with pyautogui simulation...")
    x3, y3 = 800, 300
    x4, y4 = 400, 500
    
    # 启动移动动画
    show_move_to(x3, y3, x4, y4, duration_ms=1500)
    
    # 模拟移动完成后的点击动画（延迟1.5秒）
    QTimer.singleShot(1500, lambda: show_click(x4, y4))
    
    # 保持主程序运行，等待所有动画完成
    print("\nWaiting for all animations to complete...")
    loop = QEventLoop()
    # 等待足够长的时间，确保所有动画都完成（最长的动画是2000ms + 清理时间）
    QTimer.singleShot(4000, loop.quit)
    loop.exec()
    
    print("All animations completed, exiting test.")
