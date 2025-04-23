
"""
qdown - Client for QualitegDrive

使用方法:
  qdown ID [オプション]

オプション:
  -O FILENAME     出力ファイル名を指定
  -o DIR          出力ディレクトリを指定
  -s SERVER       サーバーURLを指定 (デフォルト: https://drive.qualiteg.com)
  -q, --quiet     進捗表示を非表示
  -h, --help      ヘルプを表示
"""

import httpx
import os
import sys
import argparse
import asyncio
from pathlib import Path
from tqdm import tqdm


class QDown:
    """
    ID認証付きファイルサーバー用のPythonクライアント
    """

    def __init__(self, server_url="https://drive.qualiteg.com", quiet=False):
        """
        クライアントの初期化
        
        Args:
            server_url (str): ファイルサーバーのベースURL
            quiet (bool): 進捗表示を非表示にするかどうか
        """
        self.server_url = server_url.rstrip('/')
        self.quiet = quiet
        self.timeout = httpx.Timeout(10.0, connect=60.0)
    
    async def download(self, file_id, output=None, output_dir=None):
        """
        ファイルIDを指定してファイルをダウンロード
        
        Args:
            file_id (str): ダウンロードするファイルのID (qd_id)
            output (str, optional): 出力ファイル名
            output_dir (str, optional): 出力ディレクトリ
            
        Returns:
            str: ダウンロードしたファイルのパス
        """
        url = f"{self.server_url}/download/{file_id}"
        
        # 出力ディレクトリの設定
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        else:
            output_dir = "."
            
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            # まず、ヘッド要求を送信してファイル情報を取得
            try:
                head_response = await client.head(url)
                
                if head_response.status_code == 404:
                    print(f"エラー: ID '{file_id}' のファイルが見つかりませんでした", file=sys.stderr)
                    return None
                
                if head_response.status_code != 200:
                    print(f"エラー: ステータスコード {head_response.status_code}", file=sys.stderr)
                    return None
                
                # Content-Dispositionヘッダーからファイル名を取得
                original_filename = None
                if "content-disposition" in head_response.headers:
                    cd = head_response.headers["content-disposition"]
                    if "filename=" in cd:
                        original_filename = cd.split("filename=")[1].strip('"')
                
                # 保存用のファイル名を決定
                if not output:
                    if original_filename:
                        output_filename = original_filename
                    else:
                        output_filename = f"download_{file_id}"
                else:
                    output_filename = output
                
                file_path = os.path.join(output_dir, output_filename)
                
                # ファイルサイズを取得（プログレスバー用）
                total_size = int(head_response.headers.get("content-length", 0))
                
                # ストリーミングダウンロードを開始
                async with client.stream("GET", url) as response:
                    if response.status_code != 200:
                        print(f"エラー: ダウンロード中にエラーが発生しました。ステータスコード: {response.status_code}", file=sys.stderr)
                        return None
                    
                    with open(file_path, "wb") as f:
                        if not self.quiet and total_size > 0:
                            progress_bar = tqdm(
                                total=total_size, 
                                unit="B", 
                                unit_scale=True, 
                                desc=f"ダウンロード中: {output_filename}"
                            )
                        
                        downloaded = 0
                        
                        async for chunk in response.aiter_bytes():
                            f.write(chunk)
                            if not self.quiet and total_size > 0:
                                downloaded += len(chunk)
                                progress_bar.update(len(chunk))
                        
                        if not self.quiet and total_size > 0:
                            progress_bar.close()
                
                if not self.quiet:
                    print(f"[qdown] ファイルを保存しました: {file_path}")
                return file_path
                
            except httpx.RequestError as e:
                print(f"エラー: リクエストに失敗しました - {e}", file=sys.stderr)
                return None
            except Exception as e:
                print(f"エラー: {e}", file=sys.stderr)
                return None


def main():
    parser = argparse.ArgumentParser(
        description="qdown - IDベースファイルダウンロードツール",
        add_help=False
    )
    
    parser.add_argument("id", nargs="?", help="ダウンロードするファイルのID")
    parser.add_argument("-O", dest="output", help="出力ファイル名")
    parser.add_argument("-o", dest="output_dir", help="出力ディレクトリ")
    parser.add_argument("-s", dest="server", default="https://drive.qualiteg.com", help="サーバーURL")
    parser.add_argument("-q", "--quiet", action="store_true", help="進捗表示を非表示")
    parser.add_argument("-h", "--help", action="store_true", help="ヘルプを表示")
    
    args = parser.parse_args()
    
    if args.help or not args.id:
        print(__doc__)
        sys.exit(0)
    
    client = QDown(server_url=args.server, quiet=args.quiet)
    
    result = asyncio.run(client.download(
        file_id=args.id,
        output=args.output,
        output_dir=args.output_dir
    ))
    
    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()