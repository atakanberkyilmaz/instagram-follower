#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instagram Follower Analiz Scripti
Belirli bir Instagram hesabında:
- Hesabı takip etmeyenleri bulur (one-way followers)
- Kullanıcının takip ettiği hesapları listeler
"""

import sys
import os
import json
import csv
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, TwoFactorRequired
import argparse
from typing import List, Set, Optional
import time


def get_session_path(username: str) -> str:
    """
    Session dosya yolunu döndürür
    
    Args:
        username: Kullanıcı adı
    
    Returns:
        str: Session dosya yolu
    """
    return f"{username}_session.json"


def login_to_instagram(username: str = None, password: str = None, save_session: bool = True) -> Client:
    """
    Instagram'a giriş yapar (opsiyonel, session kaydetme desteği ile)
    
    Args:
        username: Instagram kullanıcı adı (opsiyonel)
        password: Instagram şifresi (opsiyonel)
        save_session: Session kaydedilsin mi
    
    Returns:
        Client: Instagram client objesi (giriş yapılmış veya yapılmamış)
    """
    cl = Client()
    
    # Giriş bilgileri verilmemişse, giriş yapmadan devam et
    if not username or not password:
        print("[*] Giriş yapılmadan devam ediliyor (sadece açık hesaplar için)...")
        return cl
    
    session_path = get_session_path(username)
    
    # Kaydedilmiş session varsa yükle
    if os.path.exists(session_path):
        try:
            print(f"[*] Kaydedilmis session bulundu, yukleniyor...")
            cl.load_settings(session_path)
            # Session geçerli mi kontrol et
            try:
                cl.get_timeline_feed()
                print("[+] Session basariyla yuklendi!")
                return cl
            except:
                print("[!] Session gecersiz, yeni giris yapiliyor...")
                os.remove(session_path)
        except Exception as e:
            print(f"[!] Session yuklenirken hata: {e}")
            print("[*] Yeni giris yapiliyor...")
    
    try:
        print(f"[*] {username} hesabına giriş yapılıyor...")
        cl.login(username, password)
        print("[+] Giriş başarılı!")
        
        # Session kaydet
        if save_session:
            try:
                cl.dump_settings(session_path)
                print(f"[+] Session kaydedildi: {session_path}")
            except Exception as e:
                print(f"[!] Session kaydedilemedi: {e}")
        
        return cl
    except TwoFactorRequired:
        print("[!] İki faktörlü doğrulama gerekli.")
        code = input("2FA kodunu girin: ")
        cl.login(username, password, verification_code=code)
        print("[+] Giriş başarılı!")
        
        # Session kaydet
        if save_session:
            try:
                cl.dump_settings(session_path)
                print(f"[+] Session kaydedildi: {session_path}")
            except Exception as e:
                print(f"[!] Session kaydedilemedi: {e}")
        
        return cl
    except Exception as e:
        print(f"[!] Giriş hatası: {e}")
        print("[!] Giriş yapmadan devam ediliyor (sadece açık hesaplar için)...")
        return cl


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


def get_username_safe(cl: Client, user_id: str) -> str:
    """
    Güvenli bir şekilde username alır (username_from_user_id hatası için workaround)
    
    Args:
        cl: Instagram client
        user_id: User ID
    
    Returns:
        str: Username veya None
    """
    try:
        return cl.username_from_user_id(user_id)
    except (KeyError, Exception):
        # API'den 'data' anahtarı gelmedi veya başka bir hata oluştu
        # Alternatif yöntemler dene
        try:
            # user_info_by_id metodunu dene
            user_info = cl.user_info_by_id(user_id)
            return user_info.username
        except:
            try:
                # user_info metodunu dene
                user_info = cl.user_info(user_id)
                return user_info.username
            except:
                # Başarısız oldu, None döndür
                return None


def get_followers(cl: Client, username: str, require_login: bool = False) -> Set[str]:
    """
    Belirli bir kullanıcının takipçilerini getirir (giriş yapmadan da deneyebilir)
    
    Args:
        cl: Instagram client
        username: Analiz edilecek kullanıcı adı
        require_login: Giriş gerekli mi kontrolü
    
    Returns:
        Set[str]: Takipçi kullanıcı adları seti
    """
    print(f"[*] {username} hesabının takipçileri alınıyor...")
    try:
        user_id = get_user_id_safe(cl, username)
        
        # Giriş yapmadan da deneyelim (açık hesaplar için)
        try:
            followers = cl.user_followers(user_id)
            print("[+] Takipci listesi basariyla alindi!")
        except Exception as e:
            error_msg = str(e).lower()
            error_type = str(type(e).__name__)
            
            # Giriş gerektiren hatalar
            if "login" in error_msg or "LoginRequired" in error_type or "authentication" in error_msg:
                print("[!] Takipci listesini almak icin giris yapmaniz gerekiyor.")
                print("[!] Instagram API'si takipci listelerini korumali tutuyor.")
                if require_login:
                    sys.exit(1)
                return set()
            else:
                # Başka bir hata, tekrar fırlat
                print(f"[!] Beklenmeyen hata: {e}")
                raise
        
        # Username'leri güvenli bir şekilde al
        follower_usernames = set()
        failed_count = 0
        total_followers = len(followers)
        
        print(f"[*] {total_followers} takipci ID'si bulundu, username'lere ceviriliyor...")
        
        for idx, uid in enumerate(followers.keys(), 1):
            username_result = get_username_safe(cl, uid)
            if username_result:
                follower_usernames.add(username_result)
            else:
                failed_count += 1
            
            # Progress göstergesi
            if idx % 10 == 0 or idx == total_followers:
                progress = (idx / total_followers) * 100
                print(f"[*] Ilerleme: {idx}/{total_followers} ({progress:.1f}%) - {len(follower_usernames)} username alindi...", end='\r')
            
            # Rate limiting için kısa bekleme
            if len(follower_usernames) % 50 == 0:
                time.sleep(1)
        
        print()  # Yeni satır için
        
        if failed_count > 0:
            print(f"[!] {failed_count} kullanıcının username'i alınamadı (API limiti olabilir)")
        
        print(f"[+] {len(follower_usernames)} takipçi bulundu.")
        return follower_usernames
    except Exception as e:
        print(f"[!] Takipçiler alınırken hata: {e}")
        print(f"[!] Hata detayı: {type(e).__name__}")
        if require_login:
            import traceback
            traceback.print_exc()
            sys.exit(1)
        return set()


def get_following(cl: Client, username: str, require_login: bool = False) -> Set[str]:
    """
    Belirli bir kullanıcının takip ettiği hesapları getirir (giriş yapmadan da deneyebilir)
    
    Args:
        cl: Instagram client
        username: Analiz edilecek kullanıcı adı
        require_login: Giriş gerekli mi kontrolü
    
    Returns:
        Set[str]: Takip edilen kullanıcı adları seti
    """
    print(f"[*] {username} hesabının takip ettikleri alınıyor...")
    try:
        user_id = get_user_id_safe(cl, username)
        
        # Giriş yapmadan da deneyelim (açık hesaplar için)
        try:
            following = cl.user_following(user_id)
            print("[+] Takip edilen listesi basariyla alindi!")
        except Exception as e:
            error_msg = str(e).lower()
            error_type = str(type(e).__name__)
            
            # Giriş gerektiren hatalar
            if "login" in error_msg or "LoginRequired" in error_type or "authentication" in error_msg:
                print("[!] Takip edilen listesini almak icin giris yapmaniz gerekiyor.")
                print("[!] Instagram API'si takip edilen listelerini korumali tutuyor.")
                if require_login:
                    sys.exit(1)
                return set()
            else:
                # Başka bir hata, tekrar fırlat
                print(f"[!] Beklenmeyen hata: {e}")
                raise
        
        # Username'leri güvenli bir şekilde al
        following_usernames = set()
        failed_count = 0
        total_following = len(following)
        
        print(f"[*] {total_following} takip edilen ID'si bulundu, username'lere ceviriliyor...")
        
        for idx, uid in enumerate(following.keys(), 1):
            username_result = get_username_safe(cl, uid)
            if username_result:
                following_usernames.add(username_result)
            else:
                failed_count += 1
            
            # Progress göstergesi
            if idx % 10 == 0 or idx == total_following:
                progress = (idx / total_following) * 100
                print(f"[*] Ilerleme: {idx}/{total_following} ({progress:.1f}%) - {len(following_usernames)} username alindi...", end='\r')
            
            # Rate limiting için kısa bekleme
            if len(following_usernames) % 50 == 0:
                time.sleep(1)
        
        print()  # Yeni satır için
        
        if failed_count > 0:
            print(f"[!] {failed_count} kullanıcının username'i alınamadı (API limiti olabilir)")
        
        print(f"[+] {len(following_usernames)} takip edilen hesap bulundu.")
        return following_usernames
    except Exception as e:
        print(f"[!] Takip edilenler alınırken hata: {e}")
        print(f"[!] Hata detayı: {type(e).__name__}")
        if require_login:
            import traceback
            traceback.print_exc()
            sys.exit(1)
        return set()


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


def export_to_csv(filename: str, data: List[str], title: str):
    """
    Sonuçları CSV formatında kaydeder
    
    Args:
        filename: Kayıt edilecek dosya adı
        data: Kaydedilecek veri listesi
        title: Dosya başlığı
    """
    csv_filename = filename.replace('.txt', '.csv') if filename.endswith('.txt') else f"{filename}.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([title])
        writer.writerow(['Sira', 'Kullanici Adi'])
        for i, username in enumerate(data, 1):
            writer.writerow([i, username])
    print(f"[+] CSV dosyasi kaydedildi: {csv_filename}")


def export_to_json(filename: str, data: List[str], title: str, metadata: dict = None):
    """
    Sonuçları JSON formatında kaydeder
    
    Args:
        filename: Kayıt edilecek dosya adı
        data: Kaydedilecek veri listesi
        title: Dosya başlığı
        metadata: Ek bilgiler
    """
    json_filename = filename.replace('.txt', '.json') if filename.endswith('.txt') else f"{filename}.json"
    export_data = {
        'title': title,
        'total_count': len(data),
        'data': data,
        'exported_at': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    if metadata:
        export_data['metadata'] = metadata
    
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)
    print(f"[+] JSON dosyasi kaydedildi: {json_filename}")


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
    
    parser.add_argument('-u', '--username', required=False,
                       help='Instagram kullanıcı adınız (giriş için, opsiyonel)')
    parser.add_argument('-p', '--password', required=False,
                       help='Instagram şifreniz (giriş için, opsiyonel)')
    parser.add_argument('-t', '--target', required=True,
                       help='Analiz edilecek hedef Instagram kullanıcı adı')
    parser.add_argument('--non-followers-only', action='store_true',
                       help='Sadece takip etmeyenleri göster')
    parser.add_argument('--following-only', action='store_true',
                       help='Sadece takip edilenleri göster')
    parser.add_argument('--export', choices=['csv', 'json', 'both'],
                       help='Sonuclari export et (csv, json, veya both)')
    parser.add_argument('--no-session', action='store_true',
                       help='Session kaydetme (giris yaparken)')
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("Instagram Follower Analiz Aracı")
    print("=" * 50)
    print()
    
    # Giriş yap (opsiyonel)
    save_session = not args.no_session
    cl = login_to_instagram(args.username, args.password, save_session=save_session)
    is_logged_in = args.username and args.password
    
    if not is_logged_in:
        print("[!] UYARI: Giriş yapılmadı!")
        print("[*] Giriş yapmadan takipci ve takip edilen listelerini almaya calisiyoruz...")
        print("[*] Not: Instagram genellikle bu bilgileri korumali tutar, giris gerekebilir.")
        print()
    
    # Rate limiting için bekleme
    time.sleep(2)
    
    # Takipçileri ve takip edilenleri al
    followers = set()
    following = set()
    
    if not args.following_only:
        followers = get_followers(cl, args.target, require_login=is_logged_in)
        time.sleep(2)
    
    if not args.non_followers_only:
        following = get_following(cl, args.target, require_login=is_logged_in)
        time.sleep(2)
    
    # Giriş yapılmamışsa ve hiçbir veri alınamamışsa, hesap bilgilerini göster
    if not is_logged_in and len(followers) == 0 and len(following) == 0:
        try:
            print(f"[*] {args.target} hesabının bilgileri alınıyor...")
            user_info = cl.user_info_by_username_v1(args.target)
            print(f"\n[+] Hesap Bilgileri:")
            print(f"  Kullanıcı Adı: {user_info.username}")
            print(f"  Tam Ad: {user_info.full_name}")
            print(f"  Takipçi Sayısı: {user_info.follower_count:,}")
            print(f"  Takip Edilen Sayısı: {user_info.following_count:,}")
            print(f"  Gönderi Sayısı: {user_info.media_count:,}")
            print(f"  Biyografi: {user_info.biography}")
            print(f"\n[!] Not: Takipçi ve takip edilen listelerini gormek icin giris yapmaniz gerekiyor.")
        except Exception as e:
            print(f"[!] Hesap bilgileri alinamadi: {e}")
    
    # Karşılaştırma ve sonuçları CMD'de göster
    print("\n" + "=" * 60)
    print("KARSILASTIRMA SONUCLARI")
    print("=" * 60)
    
    if len(followers) > 0 and len(following) > 0:
        print(f"\n[*] Toplam takipci sayisi: {len(followers)}")
        print(f"[*] Toplam takip edilen sayisi: {len(following)}")
        
        # Karşılaştırma yap
        print(f"\n[*] Karsilastirma yapiliyor...")
        non_followers = find_non_followers(followers, following)
        
        print(f"\n[+] SONUC: {len(non_followers)} kisi sizi takip etmiyor!")
        print("=" * 60)
        
        if non_followers:
            print(f"\n[*] Takip ettiginiz ancak sizi takip etmeyen hesaplar:\n")
            for i, username in enumerate(non_followers, 1):
                print(f"  {i:4d}. {username}")
            
            print(f"\n[*] Toplam: {len(non_followers)} hesap")
        else:
            print("\n[+] Harika! Tum takip ettikleriniz sizi de takip ediyor!")
    
    elif len(following) > 0:
        following_list = sorted(list(following))
        print(f"\n[*] {args.target} hesabinin takip ettigi hesaplar: {len(following_list)}")
        print("\n[+] Takip edilenler:\n")
        for i, username in enumerate(following_list, 1):
            print(f"  {i:4d}. {username}")
        
        # Export işlemi
        if args.export:
            metadata = {
                'target_username': args.target,
                'total_following': len(following_list)
            }
            if args.export in ['csv', 'both']:
                export_to_csv(f"{args.target}_following", following_list,
                             f"{args.target} hesabinin takip ettigi hesaplar")
            if args.export in ['json', 'both']:
                export_to_json(f"{args.target}_following", following_list,
                              f"{args.target} hesabinin takip ettigi hesaplar", metadata)
    
    elif len(followers) > 0:
        followers_list = sorted(list(followers))
        print(f"\n[*] {args.target} hesabinin takipcileri: {len(followers_list)}")
        print("\n[+] Takipciler:\n")
        for i, username in enumerate(followers_list, 1):
            print(f"  {i:4d}. {username}")
        
        # Export işlemi
        if args.export:
            metadata = {
                'target_username': args.target,
                'total_followers': len(followers_list)
            }
            if args.export in ['csv', 'both']:
                export_to_csv(f"{args.target}_followers", followers_list,
                             f"{args.target} hesabinin takipcileri")
            if args.export in ['json', 'both']:
                export_to_json(f"{args.target}_followers", followers_list,
                              f"{args.target} hesabinin takipcileri", metadata)
    
    print("\n" + "=" * 60)
    
    print("\n[+] Analiz tamamlandı!")


if __name__ == "__main__":
    main()

