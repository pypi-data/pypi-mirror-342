from dataclasses import dataclass, field, fields
from typing import Any, Optional

from aresti.sanoma import RestSanoma
from aresti.tyokalut import ei_syotetty, Valinnainen


@dataclass(kw_only=True)
class Hahmo:
  rajapinta: 'aresti.rajapinta.Rajapinta'
  pk: Valinnainen[Any] = ei_syotetty
  kwargs: dict = field(default_factory=dict)

  # Alustetaan ensimmäisellä await- tai aiter-pyynnöllä.
  tietue: Valinnainen[RestSanoma] = ei_syotetty

  tallenna_tietue: bool = True
  tuhoa_tietue: bool = False

  # def __getattr__(self, avain):
  #   return getattr(self.tietue, avain)

  # def __setattr__(self, avain, arvo):
  #   if avain in (f.name for f in fields(self)):
  #     return super().__setattr__(avain, arvo)
  #   return setattr(self.tietue, avain, arvo)

  # def __str__(self):
  #   return str(self.tietue)

  async def _await(self):
    if self.tietue is ei_syotetty:
      if self.pk:
        if self.kwargs:
          self.tietue = await self.rajapinta.muuta(
            pk=self.pk,
            data=self.rajapinta.Paivitys(**self.kwargs),
          )
        else:
          self.tietue = await self.rajapinta.nouda(
            pk=self.pk,
          )
      else:
        self.tietue = await self.rajapinta.lisaa(
          data=self.rajapinta.Syote(**self.kwargs),
        )
      self.pk = getattr(
        self.tietue,
        self.rajapinta.Meta.pk,
        ei_syotetty,
      ) or self.pk
      # if self.tietue is None
    return self.tietue
    # async def _await

  def __await__(self):
    return self._await().__await__()

  async def __aenter__(self):
    return await self

  async def __aexit__(self, exc_type, exc_value, traceback):
    if exc_type is None:
      if self.tallenna_tietue:
        await self.tallenna()
      elif self.tuhoa_tietue:
        await self.tuhoa()
    self.tietue = ei_syotetty
    # async def __aexit__

  async def __aiter__(self):
    # async def _aiter():

    if 'pk' in self.kwargs:
      tulos = await self.rajapinta.nouda(**self.kwargs)
      if tulos is not None:
        yield tulos
    else:
      async for tulos in self.rajapinta.nouda(**self.kwargs):
        yield tulos

    # async for tietue in _aiter():
    #   yield self.__class__(
    #     rajapinta=self.rajapinta,
    #     pk=getattr(tietue, self.rajapinta.Meta.pk, ei_syotetty),
    #     tietue=tietue,
    #   )
    # def __aiter__

  async def tallenna(self):
    if self.tietue is ei_syotetty:
      raise ValueError('Tietue puuttuu')
    if self.pk:
      self.tietue = await self.rajapinta.muuta(
        pk=self.pk,
        data=self.rajapinta.Paivitys.kopioi(self.tietue),
      )
    else:
      self.tietue = await self.rajapinta.lisaa(
        data=self.rajapinta.Syote.kopioi(self.tietue),
      )
    self.pk = getattr(
      self.tietue,
      self.rajapinta.Meta.pk,
      ei_syotetty,
    ) or self.pk
    # async def tallenna

  async def tuhoa(self):
    if not self.pk:
      raise ValueError('Primääriavain puuttuu')
    await self.rajapinta.tuhoa(pk=self.pk)
    self.pk = self.tietue = ei_syotetty
    # async def tuhoa

  # class Hahmo
