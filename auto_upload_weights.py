"""
AI 가중치 자동 업로드 스크립트
- 다운로드 폴더의 ai_weights.json 감지
- 학습데이터 폴더에 복사 + 프로젝트 루트에 복사
- Git 자동 커밋 & 푸시

사용법: python auto_upload_weights.py
"""

import os
import shutil
import time
import subprocess
from pathlib import Path
from datetime import datetime

# 설정
DOWNLOADS_FOLDER = Path.home() / "Downloads"
PROJECT_FOLDER = Path(r"C:\gemini\원카드")
LEARNING_DATA_FOLDER = PROJECT_FOLDER / "학습데이터"
WEIGHTS_FILENAME = "ai_weights.json"

# 학습데이터 폴더 생성
LEARNING_DATA_FOLDER.mkdir(exist_ok=True)

def get_latest_weights_file():
    """다운로드 폴더에서 가장 최근 ai_weights.json 찾기"""
    weights_files = list(DOWNLOADS_FOLDER.glob("ai_weights*.json"))
    if not weights_files:
        return None
    # 가장 최근 파일 반환
    return max(weights_files, key=lambda f: f.stat().st_mtime)

def copy_weights(source_file):
    """가중치 파일을 목적지에 복사"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 1. 학습데이터 폴더에 타임스탬프 붙여서 보관
    backup_name = f"ai_weights_{timestamp}.json"
    backup_path = LEARNING_DATA_FOLDER / backup_name
    shutil.copy2(source_file, backup_path)
    print(f"✅ 백업 저장: {backup_path}")
    
    # 2. 프로젝트 루트에 현재 가중치로 복사
    dest_path = PROJECT_FOLDER / WEIGHTS_FILENAME
    shutil.copy(source_file, dest_path)
    print(f"✅ 프로젝트 저장: {dest_path}")
    
    # 3. 원본 파일 삭제 (다운로드 폴더 정리)
    source_file.unlink()
    print(f"🗑️ 원본 삭제: {source_file}")
    
    return dest_path

def git_push():
    """Git 커밋 & 푸시"""
    try:
        os.chdir(PROJECT_FOLDER)
        
        # git add
        subprocess.run(["git", "add", WEIGHTS_FILENAME], check=True)
        
        # git commit
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_msg = f"AI 가중치 자동 업데이트 ({timestamp})"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        
        # git push
        result = subprocess.run(["git", "push"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"🚀 GitHub 푸시 완료!")
            return True
        else:
            print(f"❌ 푸시 실패: {result.stderr}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Git 오류: {e}")
        return False

def main():
    print("=" * 50)
    print("🧠 AI 가중치 자동 업로드 스크립트")
    print("=" * 50)
    print(f"📁 감시 폴더: {DOWNLOADS_FOLDER}")
    print(f"📁 저장 폴더: {LEARNING_DATA_FOLDER}")
    print(f"📁 프로젝트: {PROJECT_FOLDER}")
    print("-" * 50)
    print("⏳ ai_weights.json 파일 대기 중...")
    print("   (Ctrl+C로 종료)")
    print("-" * 50)
    
    last_processed = None
    
    while True:
        try:
            weights_file = get_latest_weights_file()
            
            if weights_file and weights_file != last_processed:
                # 파일이 완전히 다운로드될 때까지 대기
                time.sleep(1)
                
                file_mtime = weights_file.stat().st_mtime
                if last_processed is None or file_mtime > (last_processed.stat().st_mtime if last_processed.exists() else 0):
                    print(f"\n📥 새 파일 감지: {weights_file.name}")
                    
                    # 복사
                    dest = copy_weights(weights_file)
                    
                    # Git 푸시
                    if git_push():
                        print("\n✅ 모든 작업 완료!")
                        print(f"   → 백업: {LEARNING_DATA_FOLDER}")
                        print(f"   → GitHub에 업로드됨")
                    
                    last_processed = dest
                    print("\n⏳ 다음 파일 대기 중...")
            
            time.sleep(2)  # 2초마다 확인
            
        except KeyboardInterrupt:
            print("\n\n👋 스크립트 종료")
            break
        except Exception as e:
            print(f"⚠️ 오류: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
