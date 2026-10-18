#include <Wire.h>
#include <AESLib.h>
#include <time.h>

#define EEPROM_I2C_ADDR 0x50
#define EEPROM_PAGE_DELAY_MS 5

AESLib aesLib;

byte aesKey[16];
byte aesIvSeed[16] = {0}; 
void eepromWriteByte(unsigned int addr, byte data) {
  Wire.beginTransmission(EEPROM_I2C_ADDR);
  Wire.write((int)(addr >> 8));   
  Wire.write((int)(addr & 0xFF));
  Wire.write(data);
  Wire.endTransmission();
  delay(EEPROM_PAGE_DELAY_MS); 
}
byte eepromReadByte(unsigned int addr) {
  Wire.beginTransmission(EEPROM_I2C_ADDR);
  Wire.write((int)(addr >> 8));
  Wire.write((int)(addr & 0xFF));
  Wire.endTransmission();
  Wire.requestFrom(EEPROM_I2C_ADDR, 1);
  if (Wire.available()) {
    return Wire.read();
  }
  return 0xFF;
}
void eepromWriteBlock(unsigned int addr, const byte* data, int len) {
  for (int i = 0; i < len; i++) {
    eepromWriteByte(addr + i, data[i]);
  }
}
void eepromReadBlock(unsigned int addr, byte* buffer, int len) {
  for (int i = 0; i < len; i++) {
    buffer[i] = eepromReadByte(addr + i);
  }
}
void generateAesKey() {
  srand(time(0));
  for (int i = 0; i < 16; i++) {
    aesKey[i] = (byte)(rand() % 256);
  }
}
void encryptAndStore(const String &plainText, unsigned int eepromAddr) {
  int rawLen = plainText.length() + 1; 
  int paddedLen = ((rawLen / 16) + 1) * 16; 

  byte plainBuf[paddedLen];
  memset(plainBuf, 0, paddedLen);
  plainText.getBytes(plainBuf, rawLen);

  byte cipherBuf[paddedLen];
  byte iv[16];
  memcpy(iv, aesIvSeed, 16); 
  aesLib.encrypt(plainBuf, paddedLen, cipherBuf, aesKey, 128, iv);

  byte lenBytes[2] = { (byte)(paddedLen >> 8), (byte)(paddedLen & 0xFF) };
  eepromWriteBlock(eepromAddr, lenBytes, 2);
  eepromWriteBlock(eepromAddr + 2, cipherBuf, paddedLen);

  Serial.print("Stored encrypted string, ciphertext length: ");
  Serial.println(paddedLen);
}
String readAndDecrypt(unsigned int eepromAddr) {
  byte lenBytes[2];
  eepromReadBlock(eepromAddr, lenBytes, 2);
  int paddedLen = (lenBytes[0] << 8) | lenBytes[1];

  if (paddedLen <= 0 || paddedLen > 512) {
    Serial.println("Invalid stored length - nothing valid at this address?");
    return String("");
  }

  byte cipherBuf[paddedLen];
  eepromReadBlock(eepromAddr + 2, cipherBuf, paddedLen);

  byte plainBuf[paddedLen];
  byte iv[16];
  memcpy(iv, aesIvSeed, 16);

  //aesLib.decrypt(cipherBuf, paddedLen, plainBuf, aesKey, 128, iv);
  plainBuf[paddedLen - 1] = '\0';   
  return String((char*)plainBuf);
}
void setup() {
  Serial.begin(9600);
  delay(1000);
  Wire.begin();

  generateAesKey();

  String secret = "secret";
  unsigned int storageAddr = 0; 
  encryptAndStore(secret, storageAddr);
}

void loop() {
}
