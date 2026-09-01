"""多语言（i18n）后端工具。

站点内容（简历 / 音乐作品等）采用「同表多语言字段」方案：
每个可翻译字段带 `_en` / `_ja` 后缀字段，API 按 `?lang=` 参数返回对应语言，
未填翻译字段或缺省时回退中文原文。
"""
from __future__ import annotations

SUPPORTED_LANGS = ('zh', 'en', 'ja')

# 可翻译字段后缀
LANG_SUFFIXES = ('_en', '_ja')


def resolve_lang(request) -> str:
    """从请求解析目标语言（?lang=zh|en|ja），缺省/非法值回退 'zh'。"""
    if request is None:
        return 'zh'
    lang = request.query_params.get('lang')
    return lang if lang in SUPPORTED_LANGS else 'zh'


def localized_value(instance, field: str, lang: str):
    """取某字段在指定语言下的值；翻译字段为空时回退中文原值。"""
    if lang == 'zh':
        return getattr(instance, field, None)
    translated = getattr(instance, f'{field}_{lang}', None)
    return translated if translated else getattr(instance, field, None)


class LocalizedModelSerializerMixin:
    """为 ModelSerializer 提供按 ?lang= 参数输出本地化字段的能力。

    用法：class XSerializer(LocalizedModelSerializerMixin, serializers.ModelSerializer):
              localized_fields = ('title', 'description')
    输出始终只包含基础字段（_en/_ja 变体字段会被移除），
    并当 lang 非 zh 且翻译存在时覆盖基础字段的值。
    与 fields = '__all__' 兼容；序列化时需传入 context={'request': request}。
    """

    localized_fields: tuple = ()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        lang = resolve_lang(request)
        for field in self.localized_fields:
            for suffix in LANG_SUFFIXES:
                data.pop(f'{field}{suffix}', None)
            if lang != 'zh':
                localized = localized_value(instance, field, lang)
                if localized:
                    data[field] = localized
        return data