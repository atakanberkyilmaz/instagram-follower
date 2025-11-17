#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instagram Follower Analiz Scripti
Belirli bir Instagram hesabında:
- Hesabı takip etmeyenleri bulur (one-way followers)
- Kullanıcının takip ettiği hesapları listeler
"""

import sys
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, TwoFactorRequired
import argparse
from typing import List, Set
import time


def login_to_instagram(username: str, password: str) -> Client:
    """
    Instagram'a giriş yapar
    
    Args:
        username: Instagram kullanıcı adı
        password: Instagram şifresi
    
    Returns:
        Client: Giriş yapılmış Instagram client objesi
    """
    cl = Client()
    
    try:
        print(f"[*] {username} hesabına giriş yapılıyor...")
        cl.login(username, password)
        print("[+] Giriş başarılı!")
        return cl
    except TwoFactorRequired:
        print("[!] İki faktörlü doğrulama gerekli.")
        code = input("2FA kodunu girin: ")
        cl.login(username, password, verification_code=code)
        print("[+] Giriş başarılı!")
        return cl
    except Exception as e:
        print(f"[!] Giriş hatası: {e}")
        sys.exit(1)


def get_user_id_safe(cl: Client, username: str) -> str:
    """
    Güvenli bir şekilde user_id alır (user_id_from_username hatası için workaround)
    
    Args:
        cl: Instagram client
        username: Kullanıcı adı
    
    Returns:
        str: User ID
    """
    try:
        # Önce v1 API'yi dene
        user_info = cl.user_info_by_username_v1(username)
        return str(user_info.pk)
    except:
        try:
            # Alternatif: user_info kullan
            user_info = cl.user_info(username)
            return str(user_info.pk)
        except:
            # Son çare: user_id_from_username (hatalı olabilir ama deneyelim)
            return cl.user_id_from_username(username)


def get_followers(cl: Client, username: str) -> Set[str]:
    """
    Belirli bir kullanıcının takipçilerini getirir
    
    Args:
        cl: Instagram client
        username: Analiz edilecek kullanıcı adı
    
    Returns:
        Set[str]: Takipçi kullanıcı adları seti
    """
    print(f"[*] {username} hesabının takipçileri alınıyor...")
    try:
        user_id = get_user_id_safe(cl, username)
        followers = cl.user_followers(user_id)
        follower_usernames = {cl.username_from_user_id(uid) for uid in followers.keys()}
        print(f"[+] {len(follower_usernames)} takipçi bulundu.")
        return follower_usernames
    except Exception as e:
        print(f"[!] Takipçiler alınırken hata: {e}")
        print(f"[!] Hata detayı: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def get_following(cl: Client, username: str) -> Set[str]:
    """
    Belirli bir kullanıcının takip ettiği hesapları getirir
    
    Args:
        cl: Instagram client
        username: Analiz edilecek kullanıcı adı
    
    Returns:
        Set[str]: Takip edilen kullanıcı adları seti
    """
    print(f"[*] {username} hesabının takip ettikleri alınıyor...")
    try:
        user_id = get_user_id_safe(cl, username)
        following = cl.user_following(user_id)
        following_usernames = {cl.username_from_user_id(uid) for uid in following.keys()}
        print(f"[+] {len(following_usernames)} takip edilen hesap bulundu.")
        return following_usernames
    except Exception as e:
        print(f"[!] Takip edilenler alınırken hata: {e}")
        print(f"[!] Hata detayı: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def find_non_followers(followers: Set[str], following: Set[str]) -> List[str]:
    """
    Takip edilen ancak takip etmeyen hesapları bulur
    
    Args:
        followers: Takipçi kullanıcı adları seti
        following: Takip edilen kullanıcı adları seti
    
    Returns:
        List[str]: Takip edilen ancak takip etmeyen kullanıcı adları listesi
    """
    non_followers = following - followers
    return sorted(list(non_followers))


def save_results(filename: str, data: List[str], title: str):
    """
    Sonuçları dosyaya kaydeder
    
    Args:
        filename: Kayıt edilecek dosya adı
        data: Kaydedilecek veri listesi
        title: Dosya başlığı
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"{title}\n")
        f.write("=" * 50 + "\n\n")
        for i, username in enumerate(data, 1):
            f.write(f"{i}. {username}\n")
    print(f"[+] Sonuçlar '{filename}' dosyasına kaydedildi.")


def main():
    parser = argparse.ArgumentParser(
        description='Instagram Follower Analiz Aracı',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnek kullanım:
  python main.py -u kullanici_adi -p sifre -t hedef_kullanici
  
  python main.py -u kullanici_adi -p sifre -t hedef_kullanici --non-followers-only
        """
    )
    
    parser.add_argument('-u', '--username', required=True,
                       help='Instagram kullanıcı adınız (giriş için)')
    parser.add_argument('-p', '--password', required=True,
                       help='Instagram şifreniz')
    parser.add_argument('-t', '--target', required=True,
                       help='Analiz edilecek hedef Instagram kullanıcı adı')
    parser.add_argument('--non-followers-only', action='store_true',
                       help='Sadece takip etmeyenleri göster')
    parser.add_argument('--following-only', action='store_true',
                       help='Sadece takip edilenleri göster')
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("Instagram Follower Analiz Aracı")
    print("=" * 50)
    print()
    
    # Giriş yap
    cl = login_to_instagram(args.username, args.password)
    
    # Rate limiting için bekleme
    time.sleep(2)
    
    # Takipçileri ve takip edilenleri al
    if not args.following_only:
        followers = get_followers(cl, args.target)
        time.sleep(2)
    
    if not args.non_followers_only:
        following = get_following(cl, args.target)
        time.sleep(2)
    
    # Sonuçları göster ve kaydet
    if not args.following_only:
        non_followers = find_non_followers(followers, following)
        print(f"\n[*] {args.target} hesabını takip etmeyenler: {len(non_followers)}")
        
        if non_followers:
            print("\n[+] Takip etmeyenler:")
            for i, username in enumerate(non_followers[:20], 1):  # İlk 20'yi göster
                print(f"  {i}. {username}")
            if len(non_followers) > 20:
                print(f"  ... ve {len(non_followers) - 20} tane daha")
            
            save_results(f"{args.target}_non_followers.txt", non_followers, 
                        f"{args.target} hesabını takip etmeyenler")
        else:
            print("[+] Tüm takip edilenler sizi de takip ediyor!")
    
    if not args.non_followers_only:
        following_list = sorted(list(following))
        print(f"\n[*] {args.target} hesabının takip ettiği hesaplar: {len(following_list)}")
        
        print("\n[+] Takip edilenler (ilk 20):")
        for i, username in enumerate(following_list[:20], 1):
            print(f"  {i}. {username}")
        if len(following_list) > 20:
            print(f"  ... ve {len(following_list) - 20} tane daha")
        
        save_results(f"{args.target}_following.txt", following_list,
                    f"{args.target} hesabının takip ettiği hesaplar")
    
    print("\n[+] Analiz tamamlandı!")


if __name__ == "__main__":
    main()

